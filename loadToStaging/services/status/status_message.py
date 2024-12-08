from services.status.service_status import ServiceStatus

status_message = {
    ServiceStatus.RE: 'Ready extract',
    ServiceStatus.EX: 'Extracting',
    ServiceStatus.SE: 'Successful extract',
    ServiceStatus.FE: 'Failed extract',
    ServiceStatus.RP: 'Ready process',
    ServiceStatus.PX: 'Processing',
    ServiceStatus.SP: 'Successful process',
    ServiceStatus.FP: 'Failed process',
    ServiceStatus.RT: 'Ready transform',
    ServiceStatus.TX: 'Transforming',
    ServiceStatus.ST: 'Successful transform',
    ServiceStatus.FT: 'Failed transform',
    ServiceStatus.RL: 'Ready load',
    ServiceStatus.LX: 'Loading',
    ServiceStatus.SL: 'Successful load',
    ServiceStatus.FL: 'Failed load'
}