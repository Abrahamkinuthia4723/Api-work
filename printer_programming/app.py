import base64

# Function to handle animation-related operations (programming, deleting, etc.)
def animation_operations(action: str, name: str = "", additional_params: dict = {}) -> str:
    """
    Generate the XML packet for animation-related operations such as deleting, reading checksum, setting active, etc.
    
    :param action: The action to perform ('delete', 'readcrc', 'setactive', 'hide', 'deleteall', 'readlist', 'readactive', 'programmplaylist')
    :param name: The name of the animation (required for some actions like 'delete', 'readcrc', 'setactive')
    :param additional_params: Additional parameters for specific actions like 'readlist', 'readactive', etc.
    :return: The XML packet as a string.
    """
    if action not in ["delete", "readcrc", "setactive", "hide", "deleteall", "readlist", "readactive", "programmplaylist"]:
        raise ValueError(f"Invalid action: {action}")

    packet = f'<packet><animation action="{action}"'
    if name:
        packet += f' name="{name}"'

    # Handling for 'programmplaylist' action (used for scheduling animations)
    if action == "programmplaylist":
        packet += f'id="{additional_params.get("id", 0)}" datetimestart="{additional_params.get("datetimestart", "")}" '
        packet += f'datetimestop="{additional_params.get("datetimestop", "")}" name="{additional_params.get("name", "")}" '
        packet += f'day="{additional_params.get("day", 127)}" repeat="{additional_params.get("repeat", 1)}" '
        packet += f'active="{additional_params.get("active", 1)}" default="{additional_params.get("default", 0)}" '
        packet += f'clocksettingvertical="{additional_params.get("clocksettingvertical", 2)}" '
        packet += f'clocksettinghorizontal="{additional_params.get("clocksettinghorizontal", 0)}" '
        packet += f'clockvisible="{additional_params.get("clockvisible", 1)}" disp_date="{additional_params.get("disp_date", 22)}"'

    packet += f'></animation></packet>'
    return packet


# Function for programming the server address for the printer with online system
def program_server_address(action: str, value: str, server_type: int) -> str:
    """
    Generate the XML packet for programming or getting the server address.
    
    :param action: The action ('set' or 'get').
    :param value: The server address (empty for 'get' action).
    :param server_type: The type of server (1 for CPD, 2 for WebApi).
    :return: The XML packet as a string.
    """
    if action not in ["set", "get"]:
        raise ValueError(f"Invalid action: {action}")
    
    if action == "get":
        value = "" 
    
    return f'<packet><serweraddr action="{action}" value="{value}" type="{server_type}"></serweraddr></packet>'


# Function to program a graphic (handling both full and fragmented data)
def program_graphic(action: str, graphic_data: str, graphic_id: int, packet_type: str) -> str:
    """
    Generate a packet to program the graphic. It handles the split into fragments or all in one packet.
    
    :param action: The action ('programm', 'delete', 'read_crc', 'read').
    :param graphic_data: The hexadecimal graphic data (should be in an even number of characters).
    :param graphic_id: The graphic ID.
    :param packet_type: The type ('begin', 'next', 'end', 'all').
    :return: The XML packet as a string.
    """
    if len(graphic_data) % 2 != 0:
        graphic_data += "0"  
    
    if action == "programm":
        return f'<packet><graphic action="{action}" id="{graphic_id}" type="{packet_type}">{graphic_data}</graphic></packet>'
    
    elif action in ["delete", "read_crc"]:
        return f'<packet><graphic action="{action}" id="{graphic_id}"></graphic></packet>'
    
    elif action == "read":
        if packet_type == "begin":
            return f'<packet><graphic action="{action}" id="{graphic_id}" type="begin"></graphic>'
        elif packet_type == "next":
            return f'<packet><graphic action="{action}" id="{graphic_id}" type="next"></graphic>'
        elif packet_type == "repeat":
            return f'<packet><graphic action="{action}" id="{graphic_id}" type="repeat"></graphic>'
        elif packet_type == "end":
            return f'<packet><graphic action="{action}" id="{graphic_id}" type="end"></graphic>'
        else:
            raise ValueError("Invalid packet type for 'read' action")

    raise ValueError(f"Invalid action: {action}")


# Function to split the graphic data into fragments and send in multiple packets
def program_graphic_in_fragments(id: int, action: str, graphic_data: str, fragment_size: int = 500) -> str:
    """
    Split the graphic data into smaller packets and send as multiple fragments.
    
    :param id: The graphic ID.
    :param action: The action for programming ('programm').
    :param graphic_data: The complete graphic data (in hexadecimal).
    :param fragment_size: Size of each fragment (default is 500 characters).
    :return: A string with all the packet fragments.
    """
    total_length = len(graphic_data)
    fragments = []
    
    if total_length % 2 != 0:
        graphic_data = graphic_data + "0"  

    start_index = 0
    while start_index < total_length:
        end_index = min(start_index + fragment_size, total_length)
        fragment = graphic_data[start_index:end_index]
        
        # Determine packet type based on position in the data
        if start_index == 0:
            fragments.append(program_graphic(action, fragment, id, "begin"))
        elif end_index == total_length:
            fragments.append(program_graphic(action, fragment, id, "end"))
        else:
            fragments.append(program_graphic(action, fragment, id, "next"))
        
        start_index = end_index
    
    return "\n".join(fragments)

# Function to handle animation programming with base64 encoding
def program_animation(action: str, name: str, data: str, animation_size: int, packet_type: str) -> str:
    """
    Generate the XML packet to program an animation.
    
    :param action: The action ('programm').
    :param name: The name of the animation (with extension).
    :param data: The base64-encoded animation data.
    :param animation_size: The size of the animation in bytes.
    :param packet_type: The type ('begin', 'next', 'end').
    :return: The XML packet as a string.
    """
    return f'<packet><animation action="{action}" name="{name}" size="{animation_size}" type="{packet_type}">{data}</animation></packet>'

# Example for sending animation-related operations

# Deleting an animation
delete_animation_packet = animation_operations(action="delete", name="test.png")
print("Delete Animation Packet:", delete_animation_packet)

# Reading checksum of the animation
read_crc_packet = animation_operations(action="readcrc", name="test.png")
print("Read CRC Packet:", read_crc_packet)

# Setting an animation as active
set_active_packet = animation_operations(action="setactive", name="test.png")
print("Set Active Animation Packet:", set_active_packet)

# Hiding an active animation
hide_active_packet = animation_operations(action="hide")
print("Hide Active Animation Packet:", hide_active_packet)

# Deleting all animations
delete_all_animations_packet = animation_operations(action="deleteall")
print("Delete All Animations Packet:", delete_all_animations_packet)

# Read List of Animations
read_list_packet = animation_operations(action="readlist")
print("Read List of Animations Packet:", read_list_packet)

# Read Active Animation 
read_active_packet = animation_operations(action="readactive")
print("Read Active Animation Packet:", read_active_packet)

# Example: Programming the server address
server_address_packet = program_server_address(action="get", value="https://esb-te.mf.gov.pl:5062", server_type=1)
print("Server Address Packet:", server_address_packet)

# Example for programming graphics in fragments
graphic_id = 0
graphic_data = "ABCDEF1234567890"  #
graphic_packet = program_graphic_in_fragments(graphic_id, "programm", graphic_data, fragment_size=8)
print("Graphic Packet (in fragments):", graphic_packet)

