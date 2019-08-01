# Wireframe Magazine : Blend Better with Python
## Improving Your Workflow with Custom Python Scripts for Blender 2.80

This will later be changed to include the entire article, but for now it's a Github Markdown test zone.

```python
# The active object can be accessed by the following command.
>>> bpy.context.object
bpy.data.objects['Cube']
# Because bpy.context.object is read-only,
# setting it requires a different command.
>>> bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
```


```python
# Store the active object in a variable so we
# don't need to keep typing 'bpy.context.object'.
>>> obj = bpy.context.active
# Now let's get some properties of this object.
>>> obj.name
'Cube'
# The object type tells us what is stored in obj.data.
# In this case, obj.data is a mesh.
>>> obj.type
'MESH'
>>> obj.location
Vector((0, 0, 0))
# We can set the position of the cube easily by modifying its location.
# Watch it move in the 3d view when you enter the commands.
>>> obj.location.z = 3
>>> obj.location.z = 0
```

```python
# This little snippet will create four copies
# of the cube (assuming it is still selected).
>>> for i in range(1,5):
...    bpy.ops.object.duplicate()
...    bpy.ops.transform.translate((0, 2, 0))
```

```python
# Although it's already loaded in the Python console
# Blender's bpy module must be imported manually.
import bpy

# We can use a generator to get all selected mesh objects
selected_objects = [o for o in bpy.context.selected_objects if o.type = 'MESH']
# Alternatively, we can get all mesh objects in the scene
all_objects = [o for o in bpy.context.scene.objects if  o.type = 'MESH'

for i, obj in enumerate(all_objects):
    obj.name = 'Box_' + str(i+1)
    obj.location.z = i
```

```python
import bpy

def make_tube():
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
    bpy.ops.mesh.bevel(offset_type='PERCENT', offset_pct=30.0,
            segments=4, vertex_only=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Convert to a curve and tubify it!
    bpy.ops.object.convert(target='CURVE')
    bpy.context.object.data.bevel_depth = 0.1
    bpy.context.object.data.bevel_resolution = 2
    bpy.ops.object.shade_smooth()
    bpy.ops.object.convert(target='MESH')
    # Join back to the original object
    obj_original.select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')

# Call the function above
make_tube()
```