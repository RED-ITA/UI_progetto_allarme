

class Sensore():
    """
        |-------------------|
        |      SENSORI      |
        |-------------------|
        |  SensorPk         |    INTEGER (Primary Key, AUTOINCREMENT)  -- Unique identifier for each sensor
        |  Id               |    INTEGER  -- Modbus line ID, not unique
        |  Tipo             |    INTEGER  -- Type of sensor: 0 = motion, 1 = magnetic, 2 = vibration
        |  Data             |    TEXT     -- Date when the sensor was added
        |  Stanza           |    TEXT     -- Room name where the sensor is located
        |  Soglia           |    INTEGER  -- Threshold value for triggering the sensor
        |  Error            |    INTEGER  -- Error status: 0 = no error, 1 = error
        |  Stato            |    INTEGER  -- Sensor status: 1 = Active, 0 = Inactive
        |-------------------|
    """
    
    def __init__(self, SensorePk, Id, Tipo, Data, Stanza, Soglia, Error, Stato, parent=None) -> None:
        """OGGETTO SENSORE

        Args:
            SensorePk (INT): chiave primaria del db
            Id      (INT):       Modbus line ID, not unique
            Tipo    (TIN):     Type of sensor: 0 = motion, 1 = magnetic, 2 = vibration
            Data    (STR):     Date when the sensor was added
            Stanza  (STR):   Room name where the sensor is located
            Soglia  (INT):   Threshold value for triggering the sensor
            Error   (INT):    Error status: 0 = no error, 1 = error
            Stato   (INT):    Sensor status: 1 = Active, 0 = Inactive
            parent  (self, optional):       classe madre. Defaults to None.
        """        

        self.SensorePk = SensorePk #pk db del sensore in questione
        self.Id = Id
        self.Tipo = Tipo
        self.Data = Data
        self.Stanza = Stanza
        self.Soglia = Soglia
        if Error == 0:
            self.Error = False
        else:
            self.Error = True
        
        if Stato == 1: 
            self.Stato = True
        else:
            self.Stato = False
        
    def setErrore(self): 
        self.Error = True

