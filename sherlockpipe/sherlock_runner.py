# You might import a different local sherlock_user_properties
import sherlockpipe.sherlock_user_properties as sherlock_user_properties

from sherlockpipe.sherlock import Sherlock
from sherlockpipe.objectinfo.InputObjectInfo import InputObjectInfo
from sherlockpipe.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from sherlockpipe.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from sherlockpipe.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from sherlockpipe.objectinfo.MissionObjectInfo import MissionObjectInfo

# Build ObjectInfos from properties
object_infos = []
mission_object_infos = []
ffi_object_infos = []
ffi_coords_object_infos = []
input_object_infos = []
input_id_object_infos = []

## Adding by-sector analysis objects
for two_min_id, sectors in sherlock_user_properties.SECTOR_TWO_MIN_IDS.items():
    for sector in sectors:
        mission_object_infos.append(MissionObjectInfo(two_min_id, sector))
for ffi_id, sectors in sherlock_user_properties.SECTOR_FFI_IDS.items():
    for sector in sectors:
        ffi_object_infos.append(MissionFfiIdObjectInfo(ffi_id, sector))
for coords, sectors in sherlock_user_properties.SECTOR_FFI_COORDINATES.items():
    for sector in sectors:
        ffi_coords_object_infos.append(MissionFfiCoordsObjectInfo(coords[0], coords[1], sector))

## Adding global analysis objects
[mission_object_infos.append(MissionObjectInfo(two_min_id, sectors))
 for two_min_id, sectors in sherlock_user_properties.GLOBAL_TWO_MIN_IDS.items()]
[ffi_object_infos.append(MissionFfiIdObjectInfo(ffi_id, sectors))
 for ffi_id, sectors in sherlock_user_properties.GLOBAL_FFI_IDS.items()]
[ffi_coords_object_infos.append(MissionFfiCoordsObjectInfo(coords[0], coords[1], sectors))
 for coords, sectors in sherlock_user_properties.GLOBAL_FFI_COORDINATES.items()]
[input_object_infos.append(MissionInputObjectInfo(input_id, sherlock_user_properties.INPUT_FILES_WITH_IDS[input_id]))
                    for input_id in sherlock_user_properties.INPUT_FILES_WITH_IDS.keys()]
[input_id_object_infos.append(InputObjectInfo(file)) for file in sherlock_user_properties.INPUT_FILES]

## Set mask to object infos
for object_info in mission_object_infos:
    if object_info.mission_id() in sherlock_user_properties.TWO_MIN_MASKS.keys():
        object_info.initial_mask = sherlock_user_properties.TWO_MIN_MASKS[object_info.mission_id()]
for object_info in ffi_object_infos:
    if object_info.mission_id() in sherlock_user_properties.FFI_IDS_MASKS.keys():
        object_info.initial_mask = sherlock_user_properties.FFI_IDS_MASKS[object_info.mission_id()]
for object_info in ffi_coords_object_infos:
    key = str(object_info.ra) + "_" + str(object_info.dec)
    if key in sherlock_user_properties.FFI_COORDINATES_MASKS.keys():
        object_info.initial_mask = sherlock_user_properties.FFI_COORDINATES_MASKS[key]
for object_info in input_object_infos:
    if object_info.input_file in sherlock_user_properties.INPUT_FILES_MASKS.keys():
        object_info.initial_mask = sherlock_user_properties.INPUT_FILES_MASKS[object_info.input_file]
for object_info in input_id_object_infos:
    if object_info.mission_id() in sherlock_user_properties.INPUT_FILES_WITH_IDS_MASKS.keys():
        object_info.initial_mask = sherlock_user_properties.INPUT_FILES_WITH_IDS_MASKS[object_info.mission_id()]

## Set detrend period to object infos
for object_info in mission_object_infos:
    if object_info.mission_id() in sherlock_user_properties.TWO_MIN_INITIAL_DETREND_PERIOD.keys():
        object_info.initial_detrend_period = sherlock_user_properties.TWO_MIN_INITIAL_DETREND_PERIOD[object_info.mission_id()]
for object_info in ffi_object_infos:
    if object_info.mission_id() in sherlock_user_properties.FFI_IDS_INITIAL_DETREND_PERIOD.keys():
        object_info.initial_detrend_period = sherlock_user_properties.FFI_IDS_INITIAL_DETREND_PERIOD[object_info.mission_id()]
for object_info in ffi_coords_object_infos:
    key = str(object_info.ra) + "_" + str(object_info.dec)
    if key in sherlock_user_properties.FFI_COORDINATES_INITIAL_DETREND_PERIOD.keys():
        object_info.initial_detrend_period = sherlock_user_properties.FFI_COORDINATES_INITIAL_DETREND_PERIOD[key]
for object_info in input_object_infos:
    if object_info.input_file in sherlock_user_properties.INPUT_FILES_INITIAL_DETREND_PERIOD.keys():
        object_info.initial_detrend_period = sherlock_user_properties.INPUT_FILES_INITIAL_DETREND_PERIOD[object_info.input_file]
for object_info in input_id_object_infos:
    if object_info.mission_id() in sherlock_user_properties.INPUT_FILES_WITH_IDS_INITIAL_DETREND_PERIOD.keys():
        object_info.initial_detrend_period = sherlock_user_properties.INPUT_FILES_WITH_IDS_INITIAL_DETREND_PERIOD[object_info.mission_id()]

## Adding all object infos to same array
object_infos.extend(mission_object_infos)
object_infos.extend(ffi_object_infos)
object_infos.extend(ffi_coords_object_infos)
object_infos.extend(input_object_infos)
object_infos.extend(input_id_object_infos)
Sherlock(object_infos)\
    .setup_detrend(sherlock_user_properties.INITIAL_SMOOTH_ENABLED, sherlock_user_properties.INITIAL_HIGH_RMS_MASK,
                   sherlock_user_properties.INITIAL_HIGH_RMS_THRESHOLD, sherlock_user_properties.INITIAL_HIGH_RMS_BIN_HOURS,
                   sherlock_user_properties.DETRENDS_NUMBER,
                   sherlock_user_properties.DETREND_METHOD, sherlock_user_properties.DETREND_CORES,
                   sherlock_user_properties.AUTO_DETREND_ENABLED, sherlock_user_properties.AUTO_DETREND_RATIO,
                   sherlock_user_properties.AUTO_DETREND_METHOD)\
    .setup_transit_adjust_params(sherlock_user_properties.MAX_RUNS, sherlock_user_properties.PERIOD_PROTECT,
                                 sherlock_user_properties.PERIOD_MIN, sherlock_user_properties.PERIOD_MAX,
                                 sherlock_user_properties.BIN_MINUTES, sherlock_user_properties.CPU_CORES,
                                 sherlock_user_properties.SNR_MIN, sherlock_user_properties.SDE_MIN,
                                 sherlock_user_properties.FAP_MAX, sherlock_user_properties.MASK_MODE,
                                 sherlock_user_properties.BEST_SIGNAL_ALGORITHM,
                                 sherlock_user_properties.QUORUM_STRENGTH)\
    .run()