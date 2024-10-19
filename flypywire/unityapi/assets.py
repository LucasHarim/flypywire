
def get_address(category: str, model: str) -> str:
    return f'Assets/{category}/{model}'

class Airplanes:
    
    _category = 'Airplanes'
    
    A320 = get_address(_category, 'A320')
    BE767 = get_address(_category, 'BE767')
    B747 = get_address(_category, 'USAF747')
    B787 = get_address(_category, 'Boeing787')
    T6 = get_address(_category, 'BeechcraftT6II')
    A29 = get_address(_category, 'EmbA29')
    C172 = get_address(_category, 'Cessna172')
    F16 = get_address(_category, 'F16')
    F22 = get_address(_category, 'F22')
    JAS39Gripen = get_address(_category, 'JAS39Gripen')
    T38 = get_address(_category, 'T38')
    PA18 = get_address(_category, 'PiperPA18')

class Rotorcrafts:

    _category = 'Rotorcrafts'

    R44 = get_address(_category, 'R44')
    EC145 = get_address(_category, 'EC145')

class Gliders:

    _category = 'Gliders'
    
    Glider01 = get_address(_category, 'Glider01')

class Aerostats:

    _category = 'Aerostats'
    
    Airship01 = get_address(_category, 'Airship01')
    HotAirBalloon01 = get_address(_category, 'HotAirBalloon01')
    HotAirBalloon02 = get_address(_category, 'HotAirBalloon02')
    HotAirBalloon03 = get_address(_category, 'HotAirBalloon03')

class UAVs:

    _category = 'UAVs'

    DJIF450 = get_address(_category, 'DJIF450')
    DJIM300 = get_address(_category, 'DJIM300')
    FixedWing01 = get_address(_category, 'FixedWing01')


class Others:

    _category = 'Others'

    Aim7Sparrow = get_address(_category, 'Aim7Sparrow')
    MilitaryAirdrop = get_address(_category, 'MilitaryAirdrop')
