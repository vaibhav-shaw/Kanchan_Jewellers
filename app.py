from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_final_cost(weight: float, carats: int = 22, making_charges_percent: float = 14.0) -> dict:
    # Define rate per gram based on carat
    if carats == 24:
        rate_per_gram = 8175
    elif carats == 22:
        rate_per_gram = 7600
    elif carats == 18:
        rate_per_gram = 6540
    else:
        return {"error": "Unsupported carat value. Only 18, 22, and 24 carat rates are available."}
    
    # Calculate base cost for given weight
    base_cost = weight * rate_per_gram
    
    # Calculate making charges with 25% discount applied
    making_charges = base_cost * (making_charges_percent / 100)
    discounted_making_charges = making_charges * 0.75  # 25% discount on making charges
    
    # Calculate the cost before GST
    cost_before_gst = base_cost + discounted_making_charges
    
    # Calculate GST (3% on the cost before GST)
    gst = cost_before_gst * 0.03
    
    # Calculate final cost with GST
    final_cost = cost_before_gst + gst
    
    # Prepare result with all parameters
    result = {
        "Weight (grams)": round(weight, 2),
        "Carats": carats,
        "Rate per gram": rate_per_gram,
        "Base Cost": round(base_cost, 1),
        "Making Charges": round(making_charges, 1),
        "Discounted Making Charges": round(discounted_making_charges, 1),
        "Discount": round((making_charges - discounted_making_charges), 1),
        "Cost Before GST": round(cost_before_gst, 1),
        "GST (3%)": round(gst, 1),
        "Final Cost": round(final_cost, 1)
    }
    
    return result

@app.route('/calculate', methods=['GET'])
def calculate():
    # Get parameters from request
    weight = float(request.args.get('weight', 0))
    carats = int(request.args.get('carats', 22))
    making_charges_percent = float(request.args.get('making_charges', 14.0))
    
    # Calculate the final cost
    result = calculate_final_cost(weight, carats, making_charges_percent)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
