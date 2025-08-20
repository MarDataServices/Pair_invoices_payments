from fuzzywuzzy import fuzz

def compare_data(invoices, payments):
    matched = []
    unmatched_invoices = []
    unmatched_payments = payments.copy()
    for _, invoice in invoices.iterrows():
        match = None
        for id, payment in payments.iterrows():   
            """
                Updated:
                Make it so that transactions that are probably correct 
                are included but add a matching percentage for manual verification
            """          
            ratio = fuzz.partial_ratio(invoice['Customer Name'], payment['Payer Name'])
            if (
                invoice['Total Amount'] == payment['Amount']
                and (invoice['Invoice Number'] == payment['Reference'] or ratio > 85)
            ):
                match = payment
                matched.append({
                    'invoice_id': invoice['Invoice Number'],
                    'payment_id': payment['Transaction ID'],
                    'amount': invoice['Total Amount'],
                    'matching percentage': ratio,
                    
                })
                unmatched_payments.drop(index=id, inplace=True)
                break
            if not match:
                unmatched_invoices.append(invoice.to_dict())
        
    return matched, unmatched_invoices, list(unmatched_payments.to_dict(orient='records'))