import bpy
import os
from bpy import context, ops
from bpy_extras.io_utils import ImportHelper
from bpy.props import (
        CollectionProperty,
        StringProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        )

class ImportGcode(bpy.types.Operator, ImportHelper):
    bl_idname = "igcode.gcode"
    bl_label = "Import G-code"
    bl_description = 'Imports G-code file.'

    filter_glob : StringProperty(default="*.gcode", options={'HIDDEN'})
    filename_ext = ".gcode"

    layer_height : FloatProperty(
            name="Layer height:",
            default=0.25,
            min=0.1,
            max = 5.0,
            precision=3,
            description="Layer height")

    nozzle_dia : FloatProperty(
            name="Nozzle Diameter:",
            default=0.4,
            min=0.1,
            max = 5.0,
            precision=3,
            description="Nozzle Diameter")

    @staticmethod
    def batches(x, n):
        for i in range(0, len(x), n):
            yield x[i:i + n]

    @staticmethod
    def split_vertex(index):
        layer.data.splines[index].bezier_points[1].select_control_point = True
        ops.curve.delete(type='SEGMENT')
        ops.curve.select_all(action='DESELECT')
        index += 1

        layer.data.splines[index].bezier_points[0].select_control_point = True
        return index

    def execute(self, context):
        scene = context.scene
        import re
        from tqdm import tqdm

        batch_size = 30
        filename = self.filepath.split('/')[-1].split('.')[0]

        obj_collection = bpy.data.collections.new(filename)
        context.scene.collection.children.link(obj_collection)

        filtered_lines=[[]]
        vertices = [[]]
        count = -1

        pattern = re.compile(r'(;LAYER:|G[0|1] [F|X][a-zA-Z0-9. ]+ [E|Y][0-9. ]+\d\s$)')
        sub_pattern = re.compile(r'G(?P<G>[0|1])\s?[a-zA-Z0-9]*\sX(?P<X>[0-9.]*)\sY(?P<Y>[0-9.]*)')

        with open(self.filepath, 'r') as file:
            line = file.readline()
            while(line):
                matches = pattern.finditer(line)
                for match in matches:
                    if(line[0] == ';'):
                        count += 1
                        filtered_lines.append([])
                    else:
                        filtered_lines[count].append(line)
                line = file.readline()

        for i, layer in tqdm(enumerate(filtered_lines)):
            z = i*self.layer_height
            for j, line in enumerate(layer):
                match = sub_pattern.search(line)
                if match:
                    x = round(float(match.group('X')), 3)
                    y = round(float(match.group('Y')), 3)
                    g = int(match.group('G'))

                    if g==0:
                        if j+1 < len(layer):
                            if int(re.search(r'G([0|1])', layer[j+1]).group(1))==1:
                                vertices[i].append((g, round(x, 3), round(y, 3), z))                    
                    else:
                        vertices[i].append((g, round(x, 3), round(y, 3), z))            
                
            vertices.append([])

        count = 1
        for _batch in self.batches(vertices, batch_size):
            for _layer in _batch:
                if len(_layer)>0:
                    index = 0
                    ops.curve.primitive_bezier_curve_add(location=_layer[0][1:],radius=0, enter_editmode=True)

                    layer = context.active_object
                    layer.name = 'Layer: '+ str(count)

                    ops.curve.select_all(action='DESELECT')
                    ops.curve.select_random()
                    ops.curve.delete(type='VERT')
                    ops.curve.select_random()

                    layer.data.splines[index].bezier_points[0].handle_left_type = 'VECTOR'
                    layer.data.splines[index].bezier_points[0].handle_right_type = 'VECTOR'
                    
                    for v in tqdm(_layer):
                        ops.curve.vertex_add(location=v[1:])                
                        if(v[0]==0):
                            try:
                                index = self.split_vertex(index) 
                            except:
                                pass                           
                    
                    ops.object.editmode_toggle()
                    context.object.data.twist_mode = 'Z_UP'
                    context.object.data.bevel_depth = self.nozzle_dia

                    obj_collection.objects.link(layer)
                    bpy.data.collections[0].objects.unlink(layer)
                    
                    ops.object.select_all(action='DESELECT')            
                    count += 1
                
        print("\nEXPORTED "+ str(i) +" LAYERS TO 3D-VIEWPORT :)\n")
                    
        self.report({'INFO'}, 'Successfully imported {}'.format(filename))
        return {'FINISHED'}

