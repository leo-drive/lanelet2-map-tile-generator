import lanelet2_map_tile_generator.osmium_tool.osmium_tool as osmium_tool
import lanelet2_map_tile_generator.xml_tool.xml_tool as xml_tool
import lanelet2_map_tile_generator.data_preperation.data_preperation as data_preparation
from lanelet2_map_tile_generator.debug import Debug, DebugMessageType

import argparse
import os


def parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate map tiles for lanelet2 maps.')
    parser.add_argument(
        '--mgrs_grid',
        metavar='-M',
        type=str,
        help='100km MGRS grid that lanelet2 map is in')
    parser.add_argument(
        '--grid_edge_size',
        metavar='-S',
        type=int,
        help='wanted map tile size in meters')
    parser.add_argument(
        '--input_lanelet2_map',
        metavar='-L',
        type=str,
        help='input lanelet2 map path')
    parser.add_argument(
        '--output_folder',
        metavar='-O',
        type=str,
        help='output directory')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_argument()

    mgrs_grid = args.mgrs_grid
    grid_edge_size = args.grid_edge_size
    lanelet2_map_path = args.input_lanelet2_map
    output_folder = args.output_folder

    # Complete if missing "version" element in lanelet2_map.osm
    xml_tool.complete_missing_version_tag(lanelet2_map_path)

    # Create config file to extract osm file
    config_files = data_preparation.data_preparation(mgrs_grid, grid_edge_size, lanelet2_map_path, output_folder)
    # Extract osm file
    for config_file_path in config_files:
        is_extracted = osmium_tool.extract_osm_file(lanelet2_map_path, config_file_path,
                                                os.path.join(output_folder, "lanelet2_map.osm"))
        if not is_extracted:
            Debug.log("Failed to extract osm file.\n", DebugMessageType.ERROR)
            exit(1)

    # Complete missing elements in osm file
    xml_tool.complete_missing_elements(lanelet2_map_path, os.path.join(output_folder, "lanelet2_map.osm"))
