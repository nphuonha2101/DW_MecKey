from enum import Enum

class ServiceStatus(Enum):
    RE = 'RE' # Ready extract
    EX = 'EX' # Extracting
    SE = 'SE' # Successful extract
    FE = 'FE' # Failed extract
    RP = 'RP' # Ready process
    PX = 'PX' # Processing
    SP = 'SP' # Successful process
    FP = 'FP' # Failed process
    RT = 'RT' # Ready transform
    TX = 'TX' # Transforming
    ST = 'ST' # Successful transform
    FT = 'FT' # Failed transform
    RL = 'RL' # Ready load
    LX = 'LX' # Loading
    SL = 'SL' # Successful load
    FL = 'FL' # Failed load

    @classmethod
    def get_value(cls, enum_member):
        if isinstance(enum_member, cls):
            return enum_member.value
        else:
            raise ValueError("Provided argument is not a member of Enum class")
