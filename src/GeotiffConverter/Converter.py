import xml.etree.ElementTree as ET
from io import StringIO
import rasterio

def extract_xml_metadata(file_path: str, buffer_multiple: int = 32) -> ET.Element:
    """Extracts XML metadata from ESA SNAP GeoTIFF files.

    Reads the file in chunks to find and parse the Dimap_Document XML metadata
    section embedded in the GeoTIFF.

    Args:
        file_path: Path to the input GeoTIFF file.
        buffer_multiple: Multiplier for chunk size buffer (default: 32).

    Returns:
        ET.Element: Root element of parsed XML tree, or None if parsing fails.
    """
    chunk_size = 8192 * buffer_multiple
    xml_content = ""
    
    with open(file_path, 'rb') as file:
        found_start = False
        buffer = ""
        
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
                
            text = chunk.decode('utf-8', errors='ignore')
            buffer += text
            
            if not found_start and "<Dimap_Document" in buffer:
                found_start = True
                start_idx = buffer.find("<Dimap_Document")
                buffer = buffer[start_idx:]

            if found_start and "</Dimap_Document>" in buffer:
                end_idx = buffer.find("</Dimap_Document>") + len("</Dimap_Document>")
                xml_content = buffer[:end_idx]
                try:
                    xml_tree = ET.parse(StringIO(xml_content))
                    return xml_tree.getroot()
                except ET.ParseError as e:
                    print(f"XML parsing error: {e}")
                    return None
    
    return None

def band_metadata(img_path: str) -> list:
    """Extracts band metadata descriptions from ESA SNAP GeoTIFF.

    Parses the XML metadata to extract band descriptions from the Data_File
    elements.

    Args:
        img_path: Path to the input GeoTIFF file.

    Returns:
        list: List of band descriptions extracted from metadata.
    """
    root = extract_xml_metadata(img_path)
    band_desc = []
    if root is not None:
        for data_file in root.findall('.//Data_File'):
            band_index = data_file.find('BAND_INDEX').text
            file_path = data_file.find('DATA_FILE_PATH').attrib['href']
            meta_data = (file_path.split("/")[1].split(".")[0])
            band_desc.append(meta_data)
    return band_desc

def write_band_descriptions(input_file: str, output_file: str = None) -> None:
    """Writes band descriptions to a GeoTIFF file.

    Updates or creates a new GeoTIFF file with specified band descriptions while
    preserving all other metadata and raster data.

    Args:
        input_file: Path to input raster file.
        descriptions: List of descriptions for each band.
        output_file: Optional output path. If None, modifies input file in place.

    Raises:
        ValueError: If number of descriptions doesn't match number of bands.
    """
    mode = 'r+' if output_file is None else 'r'
    descriptions = band_metadata(input_file)
    
    with rasterio.open(input_file, mode) as src:
        meta = src.meta.copy()
        
        if len(descriptions) != src.count:
            raise ValueError(
                f"Number of descriptions ({len(descriptions)}) must match number of bands ({src.count})"
            )
            
        if output_file:
            with rasterio.open(output_file, 'w', **meta) as dst:
                for i in range(src.count):
                    dst.write(src.read(i+1), i+1)
                    dst.set_band_description(i+1, descriptions[i])
        else:
            for i in range(src.count):
                src.set_band_description(i+1, descriptions[i])
