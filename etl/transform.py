
def compare_data(invoices, payments):
    matched = []
    unmatched_invoices = []
    unmatched_payments = payments.copy()
    for _, invoice in invoices.iterrows():
        match = None
        for id, payment in payments.iterrows():

            if (
                invoice['Total Amount'] == payment['Amount']
                and (invoice['Invoice Number'] == payment['Reference'])
            ):
                match = payment
                matched.append({
                    'invoice_id': invoice['Invoice Number'],
                    'payment_id': payment['Transaction ID'],
                    'amount': invoice['Total Amount'],
                })
                unmatched_payments.drop(index=id, inplace=True)
                break
            if not match:
                unmatched_invoices.append(invoice.to_dict())
                print(invoice)
        
    return matched, unmatched_invoices, list(unmatched_payments.to_dict(orient='records'))