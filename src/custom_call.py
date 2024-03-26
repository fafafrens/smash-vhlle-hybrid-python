import sys
import hybrid_lib as hl
if __name__=='__main__':
    hl.custom_call(sys.argv[1], sys.argv[2], **dict(arg.split('=') for arg in sys.argv[3:])) 
