from pysmlib.SMlib cimport *

cdef class PyIceConn(object):
    cdef IceConn conn
    cdef object refs
    cdef PyIceConn init(self, IceConn conn)

cdef class PyIceListenObj(object):
    cdef IceListenObj obj
    cdef PyIceListenObj init(self, IceListenObj obj)
