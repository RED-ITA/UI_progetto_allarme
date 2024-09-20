"""

DB

tabella: SENSORI
--------------------------------------
nome    |  tipo     |   descrizione
--------------------------------------
Id      |  [int]    |   indirizzo modbus
Tipo    |  [int]    |   tipo di sensore [0] movimento, [1] magnetico, [2] vibrazione
Data    |  [date]   |   Data di aggiunta
Error   |  [int]    |   Stato di errore 0 o 1


tabella: VALORI
--------------------------------------
nome    |  tipo     |   descrizione
--------------------------------------
Id      |  [int]    |   indirizzo modbus
Value   |  [int]    |   Valore del sensore


tabella: SISTEMA
--------------------------------------
nome    |  tipo     |   descrizione
--------------------------------------
Allarme |  [int]    |   sensore andato ad 1
Stato   |  [int]    |   allarme accesa o spenta
Update  |  [int]    |   Aggiornamento Sensori
Error   |  [int]    |   Errore Sensore

"""