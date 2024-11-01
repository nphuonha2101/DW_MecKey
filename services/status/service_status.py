from enum import Enum

class ServiceStatus(Enum):
    RE = 'RE' # Ready extract
    SE = 'SE' # Successful extract
    FE = 'FE' # Failed extract
    RP = 'RP' # Ready process
    SP = 'SP' # Successful process
    FP = 'FP' # Failed process
    RT = 'RT' # Ready transform
    ST = 'ST' # Successful transform
    FT = 'FT' # Failed transform
    RL = 'RL' # Ready load
    SL = 'SL' # Successful load
    FL = 'FL' # Failed load
