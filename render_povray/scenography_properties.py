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
"""Declare stage set and surrounding (camera, lights, environment) properties controllable in UI"""
import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import PropertyGroup
from bpy.props import (
    FloatVectorProperty,
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
)

from .shading_properties import (
    active_texture_name_from_uilist,
    active_texture_name_from_search,
    brush_texture_update,
)

###############################################################################
# Camera POV properties.
###############################################################################
class RenderPovSettingsCamera(PropertyGroup):

    """Declare camera properties controllable in UI and translated to POV."""

    # DOF Toggle
    dof_enable: BoolProperty(
        name="Depth Of Field", description="Enable POV Depth Of Field ", default=False
    )

    # Aperture (Intensity of the Blur)
    dof_aperture: FloatProperty(
        name="Aperture",
        description="Similar to a real camera's aperture effect over focal blur (though not "
        "in physical units and independent of focal length). "
        "Increase to get more blur",
        min=0.01,
        max=1.00,
        default=0.50,
    )

    # Aperture adaptive sampling
    dof_samples_min: IntProperty(
        name="Samples Min",
        description="Minimum number of rays to use for each pixel",
        min=1,
        max=128,
        default=3,
    )

    dof_samples_max: IntProperty(
        name="Samples Max",
        description="Maximum number of rays to use for each pixel",
        min=1,
        max=128,
        default=9,
    )

    dof_variance: IntProperty(
        name="Variance",
        description="Minimum threshold (fractional value) for adaptive DOF sampling (up "
        "increases quality and render time). The value for the variance should "
        "be in the range of the smallest displayable color difference",
        min=1,
        max=100000,
        soft_max=10000,
        default=8192,
    )

    dof_confidence: FloatProperty(
        name="Confidence",
        description="Probability to reach the real color value. Larger confidence values "
        "will lead to more samples, slower traces and better images",
        min=0.01,
        max=0.99,
        default=0.20,
    )

    normal_enable: BoolProperty(name="Perturbated Camera", default=False)

    cam_normal: FloatProperty(name="Normal Strength", min=0.0, max=1.0, default=0.001)

    normal_patterns: EnumProperty(
        name="Pattern",
        description="",
        items=(
            ("agate", "Agate", ""),
            ("boxed", "Boxed", ""),
            ("bumps", "Bumps", ""),
            ("cells", "Cells", ""),
            ("crackle", "Crackle", ""),
            ("dents", "Dents", ""),
            ("granite", "Granite", ""),
            ("leopard", "Leopard", ""),
            ("marble", "Marble", ""),
            ("onion", "Onion", ""),
            ("pavement", "Pavement", ""),
            ("planar", "Planar", ""),
            ("quilted", "Quilted", ""),
            ("ripples", "Ripples", ""),
            ("radial", "Radial", ""),
            ("spherical", "Spherical", ""),
            ("spiral1", "Spiral1", ""),
            ("spiral2", "Spiral2", ""),
            ("spotted", "Spotted", ""),
            ("square", "Square", ""),
            ("tiling", "Tiling", ""),
            ("waves", "Waves", ""),
            ("wood", "Wood", ""),
            ("wrinkles", "Wrinkles", ""),
        ),
        default="agate",
    )

    turbulence: FloatProperty(name="Turbulence", min=0.0, max=100.0, default=0.1)

    scale: FloatProperty(name="Scale", min=0.0, default=1.0)

    ##################################CustomPOV Code############################
    # Only DUMMIES below for now:
    replacement_text: StringProperty(
        name="Texts in blend file",
        description="Type the declared name in custom POV code or an external .inc "
        "it points at. camera {} expected",
        default="",
    )


###############################################################################
# Light POV properties.
###############################################################################
class RenderPovSettingsLight(PropertyGroup):

    """Declare light properties controllable in UI and translated to POV."""

    # former Space properties from  removed Blender Internal
    use_limited_texture_context: BoolProperty(
        name="",
        description="Use the limited version of texture user (for ‘old shading’ mode)",
        default=True,
    )

    texture_context: EnumProperty(
        name="Texture context",
        description="Type of texture data to display and edit",
        items=(
            ("MATERIAL", "", "Show material textures", "MATERIAL", 0),  # "Show material textures"
            ("WORLD", "", "Show world textures", "WORLD", 1),  # "Show world textures"
            ("LAMP", "", "Show lamp textures", "LIGHT", 2),  # "Show lamp textures"
            (
                "PARTICLES",
                "",
                "Show particles textures",
                "PARTICLES",
                3,
            ),  # "Show particles textures"
            (
                "LINESTYLE",
                "",
                "Show linestyle textures",
                "LINE_DATA",
                4,
            ),  # "Show linestyle textures"
            (
                "OTHER",
                "",
                "Show other data textures",
                "TEXTURE_DATA",
                5,
            ),  # "Show other data textures"
        ),
        default="MATERIAL",
    )

    shadow_method: EnumProperty(
        name="Shadow",
        description="",
        items=(
            ("NOSHADOW", "No Shadow", "No Shadow"),
            ("RAY_SHADOW", "Ray Shadow", "Ray Shadow, Use ray tracing for shadow"),
        ),
        default="RAY_SHADOW",
    )

    active_texture_index: IntProperty(name="Index for texture_slots", default=0)

    use_halo: BoolProperty(
        name="Halo", description="Render spotlight with a volumetric halo", default=False
    )

    halo_intensity: FloatProperty(
        name="Halo intensity",
        description="Brightness of the spotlight halo cone",
        soft_min=0.0,
        soft_max=1.0,
        default=1.0,
    )

    shadow_ray_samples_x: IntProperty(
        name="Number of samples taken extra (samples x samples)", min=1, soft_max=64, default=1
    )

    shadow_ray_samples_y: IntProperty(
        name="Number of samples taken extra (samples x samples)", min=1, soft_max=64, default=1
    )

    shadow_ray_sample_method: EnumProperty(
        name="",
        description="Method for generating shadow samples: Adaptive QMC is fastest,"
        "Constant QMC is less noisy but slower",
        items=(
            ("ADAPTIVE_QMC", "", "Halton samples distribution", "", 0),
            ("CONSTANT_QMC", "", "QMC samples distribution", "", 1),
            (
                "CONSTANT_JITTERED",
                "",
                "Uses POV jitter keyword",
                "",
                2,
            ),  # "Show other data textures"
        ),
        default="CONSTANT_JITTERED",
    )

    use_jitter: BoolProperty(
        name="Jitter",
        description="Use noise for sampling (Constant Jittered sampling)",
        default=False,
    )


###############################################################################
# World POV properties.
###############################################################################
class RenderPovSettingsWorld(PropertyGroup):

    """Declare world properties controllable in UI and translated to POV."""

    # former Space properties from  removed Blender Internal
    use_limited_texture_context: BoolProperty(
        name="",
        description="Use the limited version of texture user (for ‘old shading’ mode)",
        default=True,
    )

    texture_context: EnumProperty(
        name="Texture context",
        description="Type of texture data to display and edit",
        items=(
            ("MATERIAL", "", "Show material textures", "MATERIAL", 0),  # "Show material textures"
            ("WORLD", "", "Show world textures", "WORLD", 1),  # "Show world textures"
            ("LIGHT", "", "Show lamp textures", "LIGHT", 2),  # "Show lamp textures"
            (
                "PARTICLES",
                "",
                "Show particles textures",
                "PARTICLES",
                3,
            ),  # "Show particles textures"
            (
                "LINESTYLE",
                "",
                "Show linestyle textures",
                "LINE_DATA",
                4,
            ),  # "Show linestyle textures"
            (
                "OTHER",
                "",
                "Show other data textures",
                "TEXTURE_DATA",
                5,
            ),  # "Show other data textures"
        ),
        default="MATERIAL",
    )

    use_sky_blend: BoolProperty(
        name="Blend Sky",
        description="Render background with natural progression from horizon to zenith",
        default=False,
    )

    use_sky_paper: BoolProperty(
        name="Paper Sky", description="Flatten blend or texture coordinates", default=False
    )

    use_sky_real: BoolProperty(
        name="Real Sky",
        description="Render background with a real horizon, relative to the camera angle",
        default=False,
    )

    horizon_color: FloatVectorProperty(
        name="Horizon Color",
        description="Color at the horizon",
        precision=4,
        step=0.01,
        min=0,
        soft_max=1,
        default=(0.050876, 0.050876, 0.050876),
        options={"ANIMATABLE"},
        subtype="COLOR",
    )

    zenith_color: FloatVectorProperty(
        name="Zenith Color",
        description="Color at the zenith",
        precision=4,
        step=0.01,
        min=0,
        soft_max=1,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="COLOR",
    )

    ambient_color: FloatVectorProperty(
        name="Ambient Color",
        description="Ambient color of the world",
        precision=4,
        step=0.01,
        min=0,
        soft_max=1,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="COLOR",
    )
    active_texture_index: IntProperty(
        name="Index for texture_slots", default=0, update=brush_texture_update
    )

###############################################################################
# Texture slots (World context) exported as POV texture properties.
###############################################################################

class WorldTextureSlot(PropertyGroup):
    """Declare world texture slot level properties for UI and translated to POV."""

    bl_idname = ("pov_texture_slots",)
    bl_description = ("Texture_slots from Blender-2.79",)

    # Adding a "real" texture datablock as property is not possible
    # (or at least not easy through a dynamically populated EnumProperty).
    # That's why we'll use a prop_search() UILayout function in texturing_gui.py.
    # So we'll assign the name of the needed texture datablock to the below StringProperty.
    texture: StringProperty(update=active_texture_name_from_uilist)
    # and use another temporary StringProperty to change the linked data
    texture_search: StringProperty(
        name="", update=active_texture_name_from_search, description="Browse Texture to be linked"
    )

    blend_factor: FloatProperty(
        name="Blend",
        description="Amount texture affects color progression of the " "background",
        soft_min=0.0,
        soft_max=1.0,
        default=1.0,
    )

    horizon_factor: FloatProperty(
        name="Horizon",
        description="Amount texture affects color of the horizon",
        soft_min=0.0,
        soft_max=1.0,
        default=1.0,
    )

    object: StringProperty(
        name="Object",
        description="Object to use for mapping with Object texture coordinates",
        default="",
    )

    offset: FloatVectorProperty(
        name="Offset",
        description=("Fine tune of the texture mapping X, Y and Z locations "),
        precision=4,
        step=0.1,
        soft_min=-100.0,
        soft_max=100.0,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="TRANSLATION",
    )

    scale: FloatVectorProperty(
        name="Size",
        subtype="XYZ",
        size=3,
        description="Set scaling for the texture’s X, Y and Z sizes ",
        precision=4,
        step=0.1,
        soft_min=-100.0,
        soft_max=100.0,
        default=(1.0, 1.0, 1.0),
        options={"ANIMATABLE"},
    )

    texture_coords: EnumProperty(
        name="Coordinates",
        description="Texture coordinates used to map the texture onto the background",
        items=(
            ("VIEW", "View", "Use view vector for the texture coordinates"),
            (
                "GLOBAL",
                "Global",
                "Use global coordinates for the texture coordinates (interior mist)",
            ),
            (
                "ANGMAP",
                "AngMap",
                "Use 360 degree angular coordinates, e.g. for spherical light probes",
            ),
            ("SPHERE", "Sphere", "For 360 degree panorama sky, spherical mapped, only top half"),
            ("EQUIRECT", "Equirectangular", "For 360 degree panorama sky, equirectangular mapping"),
            ("TUBE", "Tube", "For 360 degree panorama sky, cylindrical mapped, only top half"),
            ("OBJECT", "Object", "Use linked object’s coordinates for texture coordinates"),
        ),
        default="VIEW",
    )

    use_map_blend: BoolProperty(
        name="Blend Map", description="Affect the color progression of the background", default=True
    )

    use_map_horizon: BoolProperty(
        name="Horizon Map", description="Affect the color of the horizon", default=False
    )

    use_map_zenith_down: BoolProperty(
        name="", description="Affect the color of the zenith below", default=False
    )

    use_map_zenith_up: BoolProperty(
        name="Zenith Up Map", description="Affect the color of the zenith above", default=False
    )

    zenith_down_factor: FloatProperty(
        name="Zenith Down",
        description="Amount texture affects color of the zenith below",
        soft_min=0.0,
        soft_max=1.0,
        default=1.0,
    )

    zenith_up_factor: FloatProperty(
        name="Zenith Up",
        description="Amount texture affects color of the zenith above",
        soft_min=0.0,
        soft_max=1.0,
        default=1.0,
    )


"""
# class WORLD_TEXTURE_SLOTS_UL_layerlist(bpy.types.UIList):
#    texture_slots:

class WorldTextureSlots(bpy.props.PropertyGroup):
    index = bpy.prop.PropertyInt(name='index')
    # foo  = random prop

bpy.types.World.texture_slots = bpy.props.CollectionProperty(type=PropertyGroup)

for i in range(18):  # length of world texture slots
    world.texture_slots.add()
"""

classes = (
    RenderPovSettingsCamera,
    RenderPovSettingsLight,
    RenderPovSettingsWorld,
    WorldTextureSlot,
)


def register():
    for cls in classes:
        register_class(cls)

    bpy.types.Camera.pov = PointerProperty(type=RenderPovSettingsCamera)
    bpy.types.Light.pov = PointerProperty(type=RenderPovSettingsLight)
    bpy.types.World.pov = PointerProperty(type=RenderPovSettingsWorld)
    bpy.types.World.pov_texture_slots = CollectionProperty(type=WorldTextureSlot)


def unregister():
    del bpy.types.Camera.pov
    del bpy.types.Light.pov
    del bpy.types.World.pov
    del bpy.types.World.pov_texture_slots

    for cls in reversed(classes):
        unregister_class(cls)
