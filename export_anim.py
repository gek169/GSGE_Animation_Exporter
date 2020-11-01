# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import os

import bpy
import mathutils
import bpy_extras.io_utils

from progress_report import ProgressReport, ProgressReportSubstep


def name_compat(name):
    if name is None:
        return 'None'
    else:
        return name.replace(' ', '_')



   


def _write(context, filepath,
           EXPORT_TRI,  # ok
           EXPORT_EDGES,
           EXPORT_SMOOTH_GROUPS,
           EXPORT_SMOOTH_GROUPS_BITFLAGS,
           EXPORT_NORMALS,  # ok
           EXPORT_UV,  # ok
           EXPORT_MTL,
           EXPORT_APPLY_MODIFIERS,  # ok
           EXPORT_APPLY_MODIFIERS_RENDER,  # ok
           EXPORT_BLEN_OBS,
           EXPORT_GROUP_BY_OB,
           EXPORT_GROUP_BY_MAT,
           EXPORT_KEEP_VERT_ORDER,
           EXPORT_POLYGROUPS,
           EXPORT_CURVE_AS_NURBS,
           EXPORT_SEL_ONLY,  # ok
           EXPORT_ANIMATION,
           EXPORT_GLOBAL_MATRIX,
           EXPORT_PATH_MODE,  # Not used
           ):
    with ProgressReport(context.window_manager) as progress:
        from mathutils import Color, Vector
        import math
        """
        Basic write function. The context and options must be already set
        This can be accessed externaly
        eg.
        write( 'c:\\test\\foobar.obj', Blender.Object.GetSelected() ) # Using default options.
        """
        if EXPORT_GLOBAL_MATRIX is None:
            EXPORT_GLOBAL_MATRIX = mathutils.Matrix()
        def indices(lst, element):
            result = []
            offset = -1
            while True:
                try:
                    offset = lst.index(element, offset+1)
                except ValueError:
                    return result
                result.append(offset)
        
        def veckey3d(v):
            return round(v.x, 4), round(v.y, 4), round(v.z, 4)
            
        def colveckey3d(v):
            return round(v.r, 4), round(v.g, 4), round(v.b, 4)

        def veckey2d(v):
            return round(v[0], 4), round(v[1], 4)

        with ProgressReportSubstep(progress, 2, "Anim Export path: %r" % filepath, "Anim Export Finished") as subprogress1:
            with open(filepath, "w", encoding="utf8", newline="\n") as f:
                fw = f.write
                scene = context.scene
                fw("#GSGE Animation.\n")
                fw("#TUTORIAL: Name your objects 0, 1, 2 etc inside of blender according to how you want them arranged\n")
                fw("#In your GSGE file (I.E. which meshinstances they are.)\n")
                fw("#Then run the export script again (unless you've done that already!) and it'll export the frames correctly\n")
                fw("#For instance, if you have 6 Meshes that you want to animate in your character\n")
                fw("#simply put the meshinstance declaration lines in your GSGE file\n")
                fw("#in any order.\n")
                fw("#Then remember the order and name the objects 0, 1, 2... in the same order the meshinstances\n")
                fw("#are listed in the GSGE file.\n")
                fw("#Then, you can copy-paste the contents of this file\n")
                fw("#into your GSGE file and it will have working animations.\n")
                fw("#Note that the timing is NOT exported automatically. Manually edit it please\n")
                fw("#Please also edit the name. UntitledAnimation is awfully generic, don't you think?\n")
                fw("ANIM|UntitledAnimation|0.0166666\n")
                # Exit edit mode before exporting, so current object states are exported properly.
                if bpy.ops.object.mode_set.poll():
                    bpy.ops.object.mode_set(mode='OBJECT')

                orig_frame = scene.frame_current
                # Export an animation? YES OBVIOUSLY
                scene_frames = range(scene.frame_start, scene.frame_end + 1)  # Up to and including the end frame.

                # Loop through all frames in the scene and export.
                # progress.enter_substeps(len(scene_frames)) //What
                
                
                
                for frame in scene_frames:
                    scene.frame_set(frame, 0.0)
                    fw("FRAME\n")
                    if EXPORT_SEL_ONLY:
                        objects = context.selected_objects
                    else:
                        objects = scene.objects
                    for theobject in objects:
                        fw("#Object name is ")
                        fw(theobject.name)
                        fw("\n")
                        fw("TRANSFORM|") #start a matrix line
                        fw(theobject.name)
                        fw("|")
                        fw("%s|" % theobject.matrix_world.to_translation().x)
                        fw("%s|" % theobject.matrix_world.to_translation().z)
                        fw("%s|" % -theobject.matrix_world.to_translation().y)
                        fw("%s|" % theobject.matrix_world.to_euler().x)
                        fw("%s|" % theobject.matrix_world.to_euler().z)
                        fw("%s|" % -theobject.matrix_world.to_euler().y)
                        fw("%s|" % theobject.matrix_world.to_scale().x)
                        fw("%s|" % theobject.matrix_world.to_scale().z)
                        fw("%s|" % theobject.matrix_world.to_scale().y)
                        fw("\n")
                        # ~ fw(theobject.name) #print the name of the object first.
                        # ~ for i in range(0,16):
                            # ~ fw("|")
                            # ~ fw("%s" % (theobject.matrix_world[int(i/4)][int(i%4)]))
                        # ~ fw("\n")

                scene.frame_set(orig_frame, 0.0)

               

            subprogress1.step("Finished exporting Animation")
            # ~ progress.leave_substeps()




def save(context,
         filepath,
         *,
         use_triangles=False,
         use_edges=True,
         use_normals=False,
         use_smooth_groups=False,
         use_smooth_groups_bitflags=False,
         use_uvs=True,
         use_materials=True,
         use_mesh_modifiers=True,
         use_mesh_modifiers_render=False,
         use_blen_objects=True,
         group_by_object=False,
         group_by_material=False,
         keep_vertex_order=False,
         use_vertex_groups=False,
         use_nurbs=False,
         use_selection=True,
         use_animation=False,
         global_matrix=None,
         path_mode='AUTO'
         ):

    _write(context, filepath,
           EXPORT_TRI=use_triangles,
           EXPORT_EDGES=use_edges,
           EXPORT_SMOOTH_GROUPS=use_smooth_groups,
           EXPORT_SMOOTH_GROUPS_BITFLAGS=use_smooth_groups_bitflags,
           EXPORT_NORMALS=use_normals,
           EXPORT_UV=use_uvs,
           EXPORT_MTL=use_materials,
           EXPORT_APPLY_MODIFIERS=use_mesh_modifiers,
           EXPORT_APPLY_MODIFIERS_RENDER=use_mesh_modifiers_render,
           EXPORT_BLEN_OBS=use_blen_objects,
           EXPORT_GROUP_BY_OB=group_by_object,
           EXPORT_GROUP_BY_MAT=group_by_material,
           EXPORT_KEEP_VERT_ORDER=keep_vertex_order,
           EXPORT_POLYGROUPS=use_vertex_groups,
           EXPORT_CURVE_AS_NURBS=use_nurbs,
           EXPORT_SEL_ONLY=use_selection,
           EXPORT_ANIMATION=use_animation,
           EXPORT_GLOBAL_MATRIX=global_matrix,
           EXPORT_PATH_MODE=path_mode,
           )

    return {'FINISHED'}
