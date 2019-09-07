import json

def load_data(file):
    """Загрузка входных данных из файла"""
    with open(file, 'r') as f:
        input_data = json.load(f)
    couriers = {}
    orders = {}
    points = {}
    for depotData in input_data['depots']:
        points[depotData['point_id']] = {
            'location': [depotData['location_x'], depotData['location_y']],
            'timewindow': [0, 1439],
        }
    for courierData in input_data['couriers']:
        couriers[courierData['courier_id']] = {
            'location_x': courierData['location_x'],
            'location_y': courierData['location_y'],
            'time': 360,
        }
    for orderData in input_data['orders']:
        points[orderData['pickup_point_id']] = {
            'location': [orderData['pickup_location_x'], orderData['pickup_location_y']],
            'timewindow': [orderData['pickup_from'], orderData['pickup_to']],
            'order_time': {orderData['order_id']: orderData['pickup_from']}
        }
        points[orderData['dropoff_point_id']] = {
            'location': [orderData['dropoff_location_x'], orderData['dropoff_location_y']],
            'timewindow': [orderData['dropoff_from'], orderData['dropoff_to']],
        }
        orders[orderData['order_id']] = orderData
    return couriers, orders, points

def dist(ords, ord):
    return 10 + abs(ords[ord].get('dropoff_location_x') - ords[ord].get('pickup_location_x')) + abs(ords[ord].get('dropoff_location_y') - ords[ord].get('pickup_location_y'))

def dist_c(couriers, c, ords, ord):
    return 10 + abs(couriers[c].get('location_x') - ords[ord].get('pickup_location_x')) + abs(couriers[c].get('location_y') - ords[ord].get('pickup_location_y'))

if __name__ == "__main__":
    couriers, orders, points = load_data("data/contest_input.json")
    ords = orders.copy()
    for ord in ords:
        if ords[ord].get('dropoff_to') - ords[ord].get('pickup_from') < dist(ords, ord):
#        if ords[ord].get('dropoff_to') - ords[ord].get('pickup_from') < 10 + abs(ords[ord].get('dropoff_location_x') - ords[ord].get('pickup_location_x')) + abs(ords[ord].get('dropoff_location_y') - ords[ord].get('pickup_location_y')):
            orders.pop(ord)
#    print(couriers)
#    print(orders)
    template = {'courier_id': 0, 'action': 'pickup', 'order_id': 0, 'point_id': 0}
    ans = []
    for ord in orders:
        point_id = 0
        courier_id = 0
        time_min = 200000
        for c in couriers:
            time_out = couriers[c].get('time') + dist_c(couriers, c, ords, ord)
            if time_out > ords[ord].get('pickup_to'):
                continue
            if dist(ords, ord) + time_out > ords[ord].get('dropoff_to') or time_out > 1439:
                continue
            time = max(0, ords[ord].get('pickup_from') - time_out)
            if time < time_min:
                time_min = time
                courier_id = c
            elif time == time_min and dist_c(couriers, c, ords, ord) < dist_c(couriers, courier_id, ords, ord):
                time_min = time
                courier_id = c
            couriers[c].update({'time': time_out})
        if courier_id == 0:
            continue
        ans.append(template.copy())
        ans[-1].update({'courier_id': courier_id})
        ans[-1].update({'action': 'pickup'})
        ans[-1].update({'order_id': ord})
        ans[-1].update({'point_id': ords[ord].get('pickup_point_id')})
        ans.append(template.copy())
        ans[-1].update({'courier_id': courier_id})
        ans[-1].update({'action': 'dropoff'})
        ans[-1].update({'order_id': ord})
        ans[-1].update({'point_id': ords[ord].get('dropoff_point_id')})
    with open('contest_output.json', 'w') as f:
        f.write(str(ans))
