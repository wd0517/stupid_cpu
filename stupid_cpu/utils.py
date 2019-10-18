def set_proc_name(process_name):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(process_name) + 1)
    buff.value = process_name
    libc.prctl(15, byref(buff), 0, 0, 0)
