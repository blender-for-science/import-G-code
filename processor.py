import bpy
from bpy import ops
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, FloatProperty

class ImportGcode(bpy.types.Operator, ImportHelper):
    bl_idname = "igcode.gcode"
    bl_label = "Import G-code"
    bl_description = 'Imports G-code file.'

    filter_glob : StringProperty(default="*.gcode", options={'HIDDEN'})
    filename_ext = ".gcode"

    layer_height : FloatProperty(
            name="Layer height",
            default=0.2,
            min=0.1,
            max=5.0,
            precision=3,
            description="Layer height")

    nozzle_dia : FloatProperty(
            name="Nozzle Diameter",
            default=0.4,
            min=0.1,
            max=5.0,
            precision=3,
            description="Nozzle Diameter")

    @staticmethod
    def batches(x, n):
        for i in range(0, len(x), n):
            yield x[i:i + n]

    def execute(self, context):
        import re
        from tqdm import tqdm

        batch_size = 30
        filename = self.filepath.split('/')[-1].split('.')[0]

        obj_collection = bpy.data.collections.new(filename)
        context.scene.collection.children.link(obj_collection)

        layered_gcodes=[[]]
        vertices = [[]]

        pattern = re.compile(r';LAYER:|G[0|1]')
        sub_pattern = re.compile(r'G(?P<G>[0|1])\s?[a-zA-Z0-9.]*\sX(?P<X>[0-9.]*)\sY(?P<Y>[0-9.]*)')

        with open(self.filepath, 'r') as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                matches = pattern.finditer(line)
                for match in matches:
                    if(line[0] == ';'):
                        layered_gcodes.append([])
                    else:
                        if re.search(r'\w*[X|Y][0-9. a-zA-z]', line):
                            if re.search(r'E[0-9.]*', line):
                                layered_gcodes[-1].append(line)
                            else:
                                if i+1<len(lines):
                                    if re.search(r'E[0-9.]*', lines[i+1]):
                                        layered_gcodes[-1].append(line)

        layered_gcodes.pop(0)

        for i, layer in tqdm(enumerate(layered_gcodes)):
            z = i*self.layer_height
            for j, line in enumerate(layer):
                match = sub_pattern.search(line)
                if match:
                    x = round(float(match.group('X')), 3)
                    y = round(float(match.group('Y')), 3)
                    g = int(match.group('G'))
                    if g == 0:
                        if j+1 < len(layer):
                            if sub_pattern.search(layer[j+1]).group('G') != '0':
                                vertices[i].append((g, round(x, 3), round(y, 3), z))
                        else:
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

                    for v in tqdm(_layer[1:]):
                        ops.curve.vertex_add(location=v[1:])
                        if v[0] == 0:
                            ops.curve.select_all(action='DESELECT')
                            if len(layer.data.splines[index].bezier_points) > 1:
                                layer.data.splines[index].bezier_points[-1].select_control_point = True
                            if len(layer.data.splines[index].bezier_points) > 2:
                                layer.data.splines[index].bezier_points[-2].select_control_point = True
                            ops.curve.delete(type='SEGMENT')
                            ops.curve.select_all(action='DESELECT')
                            layer.data.splines[-1].bezier_points[-1].select_control_point = True
                            index += 1


                    ops.object.editmode_toggle()
                    context.object.data.twist_mode = 'Z_UP'
                    context.object.data.bevel_depth = self.nozzle_dia/2

                    obj_collection.objects.link(layer)
                    bpy.data.collections['Collection'].objects.unlink(layer)
                    ops.object.select_all(action='DESELECT')
                    count += 1

        print("\nEXPORTED "+ str(i) +" LAYERS TO 3D-VIEWPORT :)\n")
        self.report({'INFO'}, 'Successfully imported {}'.format(filename))
        return {'FINISHED'}
