bl_info = {
    "name": "Edge to Tube",
    "description": "Turn selected edges into a tube",
    "category": "Mesh",
    "author": "Andrew Palmer",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/andyp123/blender_addon_tutorial"
}

import bpy

# As of Blender 2.80, operator names must conform to a specific convention
# Naming the operator like this, instead of just EdgeToTube avoids errors
class Mesh_OT_EdgeToTube(bpy.types.Operator):
    """Edge to Tube"""              # Shown as hover tooltips
    bl_idname = "mesh.edge_to_tube" # Internal name in Blender
    bl_label = "Edge to Tube"       # Name shown in search etc.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj_original = bpy.context.object
        # Separate the selected mesh elements (hopefully the user selected some edges!)
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        # Get the object that was created from the selected parts
        obj_tube = bpy.context.selected_objects[1]
        bpy.ops.object.select_all(action='DESELECT')
        # Set this to the active object
        obj_tube.select_set(True)
        bpy.context.view_layer.objects.active = obj_tube
        # Enter edit mode and run bevel
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bevel(offset_type='PERCENT', offset_pct=25.0, segments=4, vertex_only=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        # Convert to a curve
        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.bevel_depth = 0.1
        bpy.context.object.data.bevel_resolution = 2
        bpy.ops.object.shade_smooth()
        bpy.ops.object.convert(target='MESH')
        # Join back to the original object
        obj_original.select_set(True)
        bpy.context.view_layer.objects.active = obj_original
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 1:
            return (context.object.mode == 'EDIT' and
                context.object.type == 'MESH')
        return False

classes = {
    Mesh_OT_EdgeToTube,
}

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

# This allows the add-on to be run directly from Blender's
# text editor without needing to be installed.
if __name__ == "__main__":
    register()