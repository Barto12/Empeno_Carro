def calculate_loan_amount(model, year, mileage, brand):
    base_amount = 10000  # Valor base para el préstamo
    depreciation_rate = (2024 - int(year)) * 0.05  # Depreciación por año
    loan_amount = base_amount * (1 - depreciation_rate) - (int(mileage) * 0.1)
    return max(loan_amount, 1000)  # Asegura que el monto no sea menor a 1000


def generate_contract(car):
    contract_text = f"""
    CONTRATO DE EMPEÑO
    ------------------------
    Fecha: {car.created_at}

    Vehículo:
    Placas: {car.plates}
    Modelo: {car.model}
    Año: {car.year}
    Kilometraje: {car.mileage}
    Marca: {car.brand}

    Monto del préstamo: ${car.loan_amount}

    El presente contrato certifica que el propietario del vehículo con las características descritas arriba ha empeñado su vehículo por el monto mencionado.

    Firma del propietario: _____________________

    Firma del prestamista: _____________________
    """
    return contract_text
