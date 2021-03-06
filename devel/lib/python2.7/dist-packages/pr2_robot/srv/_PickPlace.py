# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from pr2_robot/PickPlaceRequest.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import geometry_msgs.msg
import std_msgs.msg

class PickPlaceRequest(genpy.Message):
  _md5sum = "a1c37746ef6af94d99dcfe2dd193260b"
  _type = "pr2_robot/PickPlaceRequest"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """
std_msgs/Int32 test_scene_num
std_msgs/String object_name
std_msgs/String arm_name
geometry_msgs/Pose pick_pose
geometry_msgs/Pose place_pose

================================================================================
MSG: std_msgs/Int32
int32 data
================================================================================
MSG: std_msgs/String
string data

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
"""
  __slots__ = ['test_scene_num','object_name','arm_name','pick_pose','place_pose']
  _slot_types = ['std_msgs/Int32','std_msgs/String','std_msgs/String','geometry_msgs/Pose','geometry_msgs/Pose']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       test_scene_num,object_name,arm_name,pick_pose,place_pose

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PickPlaceRequest, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.test_scene_num is None:
        self.test_scene_num = std_msgs.msg.Int32()
      if self.object_name is None:
        self.object_name = std_msgs.msg.String()
      if self.arm_name is None:
        self.arm_name = std_msgs.msg.String()
      if self.pick_pose is None:
        self.pick_pose = geometry_msgs.msg.Pose()
      if self.place_pose is None:
        self.place_pose = geometry_msgs.msg.Pose()
    else:
      self.test_scene_num = std_msgs.msg.Int32()
      self.object_name = std_msgs.msg.String()
      self.arm_name = std_msgs.msg.String()
      self.pick_pose = geometry_msgs.msg.Pose()
      self.place_pose = geometry_msgs.msg.Pose()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      buff.write(_get_struct_i().pack(self.test_scene_num.data))
      _x = self.object_name.data
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.arm_name.data
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_14d().pack(_x.pick_pose.position.x, _x.pick_pose.position.y, _x.pick_pose.position.z, _x.pick_pose.orientation.x, _x.pick_pose.orientation.y, _x.pick_pose.orientation.z, _x.pick_pose.orientation.w, _x.place_pose.position.x, _x.place_pose.position.y, _x.place_pose.position.z, _x.place_pose.orientation.x, _x.place_pose.orientation.y, _x.place_pose.orientation.z, _x.place_pose.orientation.w))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.test_scene_num is None:
        self.test_scene_num = std_msgs.msg.Int32()
      if self.object_name is None:
        self.object_name = std_msgs.msg.String()
      if self.arm_name is None:
        self.arm_name = std_msgs.msg.String()
      if self.pick_pose is None:
        self.pick_pose = geometry_msgs.msg.Pose()
      if self.place_pose is None:
        self.place_pose = geometry_msgs.msg.Pose()
      end = 0
      start = end
      end += 4
      (self.test_scene_num.data,) = _get_struct_i().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.object_name.data = str[start:end].decode('utf-8')
      else:
        self.object_name.data = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.arm_name.data = str[start:end].decode('utf-8')
      else:
        self.arm_name.data = str[start:end]
      _x = self
      start = end
      end += 112
      (_x.pick_pose.position.x, _x.pick_pose.position.y, _x.pick_pose.position.z, _x.pick_pose.orientation.x, _x.pick_pose.orientation.y, _x.pick_pose.orientation.z, _x.pick_pose.orientation.w, _x.place_pose.position.x, _x.place_pose.position.y, _x.place_pose.position.z, _x.place_pose.orientation.x, _x.place_pose.orientation.y, _x.place_pose.orientation.z, _x.place_pose.orientation.w,) = _get_struct_14d().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      buff.write(_get_struct_i().pack(self.test_scene_num.data))
      _x = self.object_name.data
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.arm_name.data
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_14d().pack(_x.pick_pose.position.x, _x.pick_pose.position.y, _x.pick_pose.position.z, _x.pick_pose.orientation.x, _x.pick_pose.orientation.y, _x.pick_pose.orientation.z, _x.pick_pose.orientation.w, _x.place_pose.position.x, _x.place_pose.position.y, _x.place_pose.position.z, _x.place_pose.orientation.x, _x.place_pose.orientation.y, _x.place_pose.orientation.z, _x.place_pose.orientation.w))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.test_scene_num is None:
        self.test_scene_num = std_msgs.msg.Int32()
      if self.object_name is None:
        self.object_name = std_msgs.msg.String()
      if self.arm_name is None:
        self.arm_name = std_msgs.msg.String()
      if self.pick_pose is None:
        self.pick_pose = geometry_msgs.msg.Pose()
      if self.place_pose is None:
        self.place_pose = geometry_msgs.msg.Pose()
      end = 0
      start = end
      end += 4
      (self.test_scene_num.data,) = _get_struct_i().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.object_name.data = str[start:end].decode('utf-8')
      else:
        self.object_name.data = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.arm_name.data = str[start:end].decode('utf-8')
      else:
        self.arm_name.data = str[start:end]
      _x = self
      start = end
      end += 112
      (_x.pick_pose.position.x, _x.pick_pose.position.y, _x.pick_pose.position.z, _x.pick_pose.orientation.x, _x.pick_pose.orientation.y, _x.pick_pose.orientation.z, _x.pick_pose.orientation.w, _x.place_pose.position.x, _x.place_pose.position.y, _x.place_pose.position.z, _x.place_pose.orientation.x, _x.place_pose.orientation.y, _x.place_pose.orientation.z, _x.place_pose.orientation.w,) = _get_struct_14d().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_i = None
def _get_struct_i():
    global _struct_i
    if _struct_i is None:
        _struct_i = struct.Struct("<i")
    return _struct_i
_struct_14d = None
def _get_struct_14d():
    global _struct_14d
    if _struct_14d is None:
        _struct_14d = struct.Struct("<14d")
    return _struct_14d
# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from pr2_robot/PickPlaceResponse.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class PickPlaceResponse(genpy.Message):
  _md5sum = "358e233cde0c8a8bcfea4ce193f8fc15"
  _type = "pr2_robot/PickPlaceResponse"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """
bool success

"""
  __slots__ = ['success']
  _slot_types = ['bool']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       success

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PickPlaceResponse, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.success is None:
        self.success = False
    else:
      self.success = False

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      buff.write(_get_struct_B().pack(self.success))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      buff.write(_get_struct_B().pack(self.success))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_B = None
def _get_struct_B():
    global _struct_B
    if _struct_B is None:
        _struct_B = struct.Struct("<B")
    return _struct_B
class PickPlace(object):
  _type          = 'pr2_robot/PickPlace'
  _md5sum = '803571dc87b1116273df703ec8a12b59'
  _request_class  = PickPlaceRequest
  _response_class = PickPlaceResponse
