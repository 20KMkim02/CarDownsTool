from fastapi import FastAPI

app = FastAPI()

def calculate_monthly_payment(price, down_payment_percent, years, interest_rate):
    # เงินดาวน์
    down_payment = price * (down_payment_percent / 100)
    print('down_payment:',down_payment)
    # ยอดจัดไฟแนนซ์
    loan_amount = price - down_payment
    print('loan_amount:',loan_amount)
    # จำนวนเดือนที่ผ่อน
    months = years * 12
    # ดอกเบี้ยที่ต้องจ่ายทั้งหมด
    all_month_interest=(loan_amount*interest_rate*years)/100
    print('all_month_interest:',all_month_interest)
    # ค่างวดผ่อน
    monthly_payment = (all_month_interest + loan_amount) / months
    # monthly_payment=monthly_payment//1

    return monthly_payment, loan_amount

# DEBUG
# print(calculate_monthly_payment(1439000,15,7,4.29))


@app.get("/tool/request_promotion")
def use(car_model: str, years: int, down_payment_percent: int):
    # ราคาของรถแต่ละรุ่น
    car_prices = {
        "G6_standard": 1439000,
        "G6_long": 1599000
    }

    # อัตราดอกเบี้ยตามรุ่นรถ and ระยะเวลาผ่อน
    interest_rates = {
        "G6_standard": {
            4: [3.09, 2.69, 1.98, 1.98],
            5: [3.39, 2.89, 2.59, 2.39],
            6: [3.59, 3.09, 2.99, 2.89],
            7: [4.29, 3.79, 3.59, 3.49]
        },
        "G6_long": {
            4: [3.09, 2.69, 1.98, 1.98],
            5: [3.39, 2.89, 2.59, 2.39],
            6: [3.59, 3.09, 2.99, 2.89],
            7: [4.29, 3.79, 3.59, 3.49]
        }
    }

    if car_model not in car_prices:
        return "รุ่นรถไม่ถูกต้อง กรุณาเลือกจากรุ่นที่มีในระบบ (G6_standard หรือ G6_long)"

    # คำนวณราคาผ่อนและดอกเบี้ยตามเงินดาวน์ที่เลือก
    price = car_prices[car_model]
    down_payment = down_payment_percent
    if down_payment not in [15, 20, 25, 30]:
        return "เงินดาวน์ต้องเป็น 15%, 20%, 25%, หรือ 30% เท่านั้น"
    
    if years not in [4, 5, 6, 7]:
        return "จำนวนปีผ่อนต้องเป็น 4, 5, 6, หรือ 7 ปี เท่านั้น"
    
    # คำนวณดอกเบี้ยจากรุ่นรถ, ระยะเวลา และเปอร์เซ็นต์ดาวน์
    interest_rate = interest_rates[car_model][years][[15, 20, 25, 30].index(down_payment)]
    # คำนวณค่างวดผ่อน
    monthly_payment, loan_amount = calculate_monthly_payment(price, down_payment, years, interest_rate)
   
    return {
        "รุ่นรถ": car_model,
        "จำนวนปีผ่อน": years,
        "เงินดาวน์": f"{down_payment}%",
        "ยอดผ่อนไฟแนนซ์ (ต่อเดือน)": f"{monthly_payment:.2f} บาท",
        "ยอดจัดไฟแนนซ์": f"{loan_amount:.2f} บาท",
        "อัตราดอกเบี้ย": f"{interest_rate}%"
    }