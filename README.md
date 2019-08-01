# Wireframe Magazine : Blend Better with Python
## Improving Your Workflow with Custom Python Scripts for Blender 2.80

| This will later be changed to include the entire article, but for now it's a Github Markdown test zone. |

---

Blender has long been the go to 3d modelling and animation program for artists on a tight budget due to its free and open source license, but more recently, and especially with the release of Blender 2.80, is becoming known not only for its free license, but also for its power and flexibility.

Even though Blender is a tremendously powerful package out of the box, it has a rich Python 3 API, allowing users to create custom add-ons to tweak Blender's behaviour or even add entirely new features. With just a modicum of Python knowledge, you can start writing your own scripts and bending Blender to the needs of your project and personal workflow, and with this article I'm going to demonstrate how easy it is to get started.

### Playing Around in the Console

One of the easiest ways to get up and running with Python in Blender is to use the built-in Python console to quickly test commands, and the script editor to write and test code. Blender 2.80 has a default scripting workspace, where the Python console, text editor and info panel are all set up for you to begin playing around with.

First off, let's open Blender 2.80 and switch to the scripting workspace by clicking on the tab labelled 'Scripting' at the top of the window. For this exercise, you will only really need the 3d view, Python console, info window and outliner, which are shown in *Figure 1*.

The 3d view should contain three objects; The default cube, a camera and a light. If your scene doesn't contain these, either reset the default settings from the menu ('File > Defaults > Load Factory Settings') or just add the objects manually. Make sure the cube is selected.

Now let's try using the Python console to interact with the 3d view! Unlike most other applications, the active area is set by the mouse cursor being inside it, so before doing anything else, make sure the cursor is inside the console, or nothing will happen when you type.

There are two main ways to access objects; First by using the context to get objects that are active or selected, and second by using bpy.data to access objects by name or index. Most of the time, you will want to operate on something that is selected, so let's enter our first command to see what is selected.

```python
# The active object can be accessed by the following command.
>>> bpy.context.object
bpy.data.objects['Cube']
# Because bpy.context.object is read-only,
# setting it requires a different command.
>>> bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
```

The active object is usually the last object that was selected by the user, and will be highlighted in a bright yellow colour. When there are multiple objects selected, selected objects will have an orange outline, so the active object should stand out. Many operations in Blender will operate on the active object, whilst others will simply operate upon what is selected. Let’s continue…

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

As you can see, it’s quite easy to try basic commands in the console. It’s also great for discovering the properties of different object types thanks to Blender’s Autocomplete function. Simple start typing and press ‘Ctrl+Space’ to see a list of possible completions. Try it on “obj.” to see all the properties of the active object.

Now let’s try one last example in the console before we move to the script editor.

```python
# This little snippet will create four copies
# of the cube (assuming it is still selected).
>>> for i in range(1,5):
...    bpy.ops.object.duplicate()
...    bpy.ops.transform.translate((0, 2, 0))
```

### Writing a Script

The Python console is good for quickly testing commands and playing around, but once you begin to have an idea of what it is you want to do, it’s best to start working in the script editor. The script editor is a proper text editor built right into Blender, and allows you to modify files in the same way you would in any other editor, such as Notepad in Windows, or Gedit in Linux, but makes running scripts you have written much more convenient.

Move over to the script editor and click on the ‘New’ button at the top. This will create an empty file for you to enter your code. While you are up at the top, make sure that the line numbers and syntax highlighting buttons are turned on, as it will make editing your code a much more pleasant experience.

Now let’s start writing some code and test our first script!

```python
# Although it's already loaded in the Python console
# Blender's bpy module must be imported manually.
import bpy

# We can use a generator to get all selected mesh objects
selected_objects = [o for o in bpy.context.selected_objects if o.type = 'MESH']
# Alternatively, we can get all mesh objects in the scene
all_objects = [o for o in bpy.context.scene.objects if  o.type = 'MESH']

for i, obj in enumerate(all_objects):
    obj.name = 'Box_' + str(i+1)
    obj.location.z = i
```

This script can be run by pressing the button marked ‘Run Script’ in the top right of the text editor, or by pressing ‘ALT+P’. If you have entered the code correctly, the cubes that were created previously should be renamed Box_1 to Box_5 and be arranged like a staircase. Although this is not exactly the most useful script ever written, it should give you an idea of how simple it is to batch operations in a script so that they can be run on multiple objects.

### A More Useful Script

Now we’ve covered the basics, let’s try writing something a bit more useful. How about a modelling tool that makes it easy to create pipes and wires? It’s already fairly easy to create pipes and wires in Blender, but the workflow for doing so is not as smooth as it could be, so how about making a tube tool that creates a tube along a set of selected edges?

Now this may sound like a huge jump in difficulty over the previous example, and perhaps it is if we write all our own algorithms, but as I mentioned, Blender already has some tools to make pipes and wires, so we can just use the python commands these tools utilise behind the scenes to make our own tool!

As you’ve been working through the examples, you might have noticed that the info window has what looks like code printing in it each time you do something. This is actually the Python commands that are being activated, and we can copy this out of the info window to use in our own scripts. This means that if we manually perform the steps to create a tube along selected edges, the code to do so should appear in the info window! Let’s give it a try.

### Prototyping the Script

First start a new scene so that you just have the default cube, camera and light. Select the cube and enter edit mode. Now select a vertex and extrude it a few times to create a line made of multiple segments coming off it so that it looks like the image below.

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