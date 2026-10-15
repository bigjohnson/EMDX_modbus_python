import minimalmodbus
import serial
import os

SMARTMETER_ADDRESS = 5 
SMARTMETER_COMPORT = "COM3"

try:
    SMARTMETER = minimalmodbus.Instrument(SMARTMETER_COMPORT, SMARTMETER_ADDRESS)
except:
    print('non posso aprire la porta', SMARTMETER_COMPORT)
    os._exit(1)

SMARTMETER.serial.baudrate = 19200         # Baud
SMARTMETER.serial.bytesize = 8
SMARTMETER.serial.parity   = serial.PARITY_EVEN # vendor default is EVEN
SMARTMETER.serial.stopbits = 1
SMARTMETER.serial.timeout  = 1          # seconds
SMARTMETER.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
SMARTMETER.clear_buffers_before_each_transaction = True
SMARTMETER.debug = False # set to "True" for debug mode

try:
    PT = SMARTMETER.read_register(0x0, 0, 3)
    if PT == 0:
        print("0x0 Protocol type", PT, "Standard MAP" )
    elif PT == 1:
        print("0x0 Protocol type", PT, "Basic MAP" )
    else:
        print("0x0 Protocol type", PT, "Mistery" )

    EI = SMARTMETER.read_register(0x1001, 0, 3)
    if EI == 0:
        print("0x1001 Configuration of external input", EI, "Tariff selector" )
    elif EI == 0x40:
        print("0x1001 Configuration of external input", EI, "Pulse measurement" )
    else:
        print("0x1001 Configuration of external input", EI, "Mistery" )

    Current =  SMARTMETER.read_long(0x5000, 4) / 1000
    print("0x5000 Single-phase Current Value", Current, "A")

    KTA =  SMARTMETER.read_register(0x5001, 0, 3)
    print("0x5001 Phase Currents Transformation Ratio (KTA)", KTA)

    KTV =  SMARTMETER.read_register(0x5004, 0, 3) / 100
    print("0x5004 Voltage Transformation Ratio (KTV)", KTV)

    RCSR =  SMARTMETER.read_long(0x5005, 3)

    SBL = RCSR & 1
    CW = RCSR & 0xF0000
    CW = CW >> 16
    if SBL > 0:
        print ("0x5005 Sliding block interval of", CW, "seconds")
    else:
        print ("0x5005 No sliding block interval")

    Voltage =  SMARTMETER.read_long(0x501D, 4) / 1000
    print("0x501D Single-phase Voltage L-N", Voltage, "V")

    Frequency = SMARTMETER.read_register(0x5039, 2, 4)
    print("0x5039 Single-phase frequency", Frequency, "Hz")

    RawActivePower = SMARTMETER.read_long(0x5047, 4)

    ActivePower = (RawActivePower & 2147483647) / 100
    ActiveSign = RawActivePower & 2147483648

    if ActiveSign > 0:
        ActivePower = ActivePower * -1

    print("0x5047 Single-phase Active Power", ActivePower, "W")

    RawReactivePower = SMARTMETER.read_long(0x504D, 4) 

    ReactivePower = (RawReactivePower & 2147483647) / 100
    ReactiveSign = RawReactivePower & 2147483648

    if ReactiveSign > 0:
        ReactivePower = ReactivePower * -1

    print("0x504D Single-phase Reactive Power", ReactivePower, "var")

    ApparentPower = SMARTMETER.read_long(0x5059, 4) / 100
    print("0x5059 Single-phase Apparent Power", ApparentPower, "VA")

    RPF = SMARTMETER.read_register(0x5065, 0, 4)

    PF = (RPF & 32767) / 1000
    PFX = RPF & 32768

    if PFX > 0:
        PF = PF * -1

    print("0x5065 Single-phase Power Factor (PF)", PF)

    PFS = SMARTMETER.read_register(0x506B, 0, 4)

    if PFS == 1:
        print("0x506B Single-phase Power Factor (sector)", PFS, "inductive")
    elif PFS == 2:
        print("0x506B Single-phase Power Factor (sector)", PFS, "capacitive")
    else:
        print("0x506B Single-phase Power Factor (sector)", PFS, "mistery")

    PSAE = SMARTMETER.read_long(0x5070, 4) / 100
    print("0x5070 Positive Single-phase Active Energy", PSAE, "kWh")

    NSAE = SMARTMETER.read_long(0x5072, 4) / 100
    print("0x5072 Negative Single-phase Active Energy", NSAE, "kWh")

    PSRE = SMARTMETER.read_long(0x5076, 4) / 100
    print("0x5076 Positive Single-phase Reactive Energy", PSRE, "kVarh")

    NSRE = SMARTMETER.read_long(0x5078, 4) / 100
    print("0x5078 Negative Single-phase Reactive Energy", NSRE, "kVarh")

    PSAE1 = SMARTMETER.read_long(0x507C, 4) / 100
    print("0x507C Positive Single-phase Active Energy (Tariff 1)", PSAE1, "kWh")

    NSAE1 = SMARTMETER.read_long(0x507E, 4) / 100
    print("0x507E Negative Single-phase Active Energy (Tariff 1)", NSAE1, "kWh")

    PSRE1 = SMARTMETER.read_long(0x5080, 4) / 100
    print("0x5080 Positive Single-phase Reactive Energy (Tariff 1)", PSRE1, "kVarh")

    NSRE1 = SMARTMETER.read_long(0x5082, 4) / 100
    print("0x5082 Negative Single-phase Reactive Energy (Tariff 1)", NSRE1, "kVarh")

    PSAE2 = SMARTMETER.read_long(0x5084, 4) / 100
    print("0x5084 Positive Single-phase Active Energy (Tariff 2)", PSAE2, "kWh")

    NSAE2 = SMARTMETER.read_long(0x5086, 4) / 100
    print("0x5086 Negative Single-phase Active Energy (Tariff 2)", NSAE2, "kWh")

    PSRE2 = SMARTMETER.read_long(0x5088, 4) / 100
    print("0x5088 Positive Single-phase Reactive Energy (Tariff 2)", PSRE2, "kVarh")

    NSRE2 = SMARTMETER.read_long(0x508A, 4) / 100
    print("0x508A Negative Single-phase Reactive Energy (Tariff 2)", NSRE2, "kVarh")

    PPAE = SMARTMETER.read_long(0x504E, 3) / 100
    print("0x504E Partial Positive Active Energy", PPAE, "kWh")

    PPAE = SMARTMETER.read_long(0x5050, 3) / 100
    print("0x5050 Partial Negative Active Energy", PPAE, "kWh")

    PPRE = SMARTMETER.read_long(0x5054, 3) / 100
    print("0x5054 Partial Positive Reactive Energy", PPRE, "kvarh")

    PNRE = SMARTMETER.read_long(0x5056, 3) / 100
    print("0x5056 Partial Negative Reactive Energy", PNRE, "W")

    TAPR = SMARTMETER.read_long(0x509C, 3) / 100
    print("0x509C Total Active Power Requirement (MD)", TAPR, "W") 

    MTAPR = SMARTMETER.read_long(0x509E, 3) / 100
    print("0x509E Maximum Total Active Power Requirement (PMD)", MTAPR, "W") 

    MTAPR1 = SMARTMETER.read_long(0x50C0, 3) / 100
    print("0x50C0 Maximum Total Active Power Requirement Tariff 1 (PMD T1)", MTAPR1, "W") 

    MTAPR2 = SMARTMETER.read_long(0x50C6, 3) / 100
    print("0x50C6 Maximum Total Active Power Requirement Tariff 2 (PMD T2)", MTAPR2, "W") 

    RHMT = SMARTMETER.read_register(0x50D8, 2, 3) / 100
    print("0x50D8 Run hour meter threshold", RHMT, "%") 

    RHMTOT = SMARTMETER.read_long(0x50C6, 3)
    print("0x50C6 Run hour meter (TOT)", RHMTOT, "s") 

    RHMTOT1 = SMARTMETER.read_long(0x50DB, 3)
    print("0x50DB Run hour meter (Tariff 1)", RHMTOT1, "s")

    RHMTOT2 = SMARTMETER.read_long(0x50DD, 3)
    print("0x50DD Run hour meter (Tariff 2)", RHMTOT2, "s")

    MI = SMARTMETER.read_register(0x7400, 0, 3)
    print("0x7400 Measurement unit input", MI) 

    PWI = SMARTMETER.read_register(0x7401, 2, 3)
    print("0x7401 Pulse weight input", PWI) 

    PPI = SMARTMETER.read_long(0x7402, 3) / 100
    print("0x7402 Pulse pulse input", PPI)



except:
    print('non posso comunicare con il device', SMARTMETER_ADDRESS, "connesso alla porta", SMARTMETER_COMPORT)
    os._exit(1)
