from init import *
import sys, os


# FUNCTIONS-------------------------------------------------------------------------------------------------------------
def get_package(pkg_id):
    """Get Package object from its hash table

    Space Complexity O(N)
    Time Complexity O(N)
    :param pkg_id: package ID
    :return: package object
    """
    return packageHashTable.get(pkg_id)


def assigned_truck(pkg_id):
    """Assign truck priority based on notes and deadline

    Space Complexity O(1)
    Time Complexity O(1)
    :param pkg_id: package ID
    :return: assigned truck
    """
    priority_truck = 3
    if get_package(pkg_id).deadline != end_time:  # Packages with specific deadline
        priority_truck = 1
    if pkg_id in [13, 14, 15, 16, 19, 20]:  # Packages with 'Must be delivered with ' notes
        priority_truck = 1
    if 'Can only be on truck 2' in get_package(pkg_id).notes:  # Packages required on truck 2
        priority_truck = 2
    if 'Delayed on flight' in get_package(pkg_id).notes:  # Delayed packages
        priority_truck = 2
    if 'Wrong address listed' in get_package(pkg_id).notes:  # Packages with wrong address
        priority_truck = 3
    return priority_truck


def load(pkg_id, t):
    """Load package into truck t

    Space Complexity O(1)
    Time Complexity O(1)
    :param pkg_id: package ID
    :param t: truck to be loaded
    """
    packages_on_truck[t].append(pkg_id)
    available[t] -= 1
    if get_package(pkg_id).location_id not in route_for_truck[t]:
        route_for_truck[t].append(get_package(pkg_id).location_id)


def diff_distance(v1, v2, v3, v4):
    """Distance difference between 4 vertices for 2-opt algorithm validation

    Space Complexity O(1)
    Time Complexity O(1)
    :param v1: vertex 1
    :param v2: vertex 2
    :param v3: vertex 3
    :param v4: vertex 4
    :return: distance difference between current route and an alternate route
    """
    return (distance[v1][v3] + distance[v2][v4]) - (distance[v1][v2] + distance[v3][v4])


def optimized_route(route):
    """2-opt algorithm for avoiding crossing and optimize distance

    Space Complexity O(N)
    Time Complexity O(N^2)
    :param route: route to be optimized
    :return: optimized route
    """
    opt_route = route
    optimized = True
    while optimized:
        optimized = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                if diff_distance(opt_route[i - 1], opt_route[i], opt_route[j - 1], opt_route[j]) < 0:
                    opt_route[i:j] = opt_route[j - 1:i - 1:-1]
                    optimized = True
        route = opt_route
    return opt_route


def blockPrint():
    """Disable printing

    Space Complexity O(1)
    Time Complexity O(1)"""
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    """Restore printing

    Space Complexity O(1)
    Time Complexity O(1)"""
    sys.stdout = sys.__stdout__


def print_truck_header():
    """Truck simulation header - matching simulation.run() output

    Space Complexity O(1)
    Time Complexity O(1)"""
    print('-' * 91)
    print('| {:^5} | {:^5} | {:^3} | {:^8} | {:^5} | {:^7} | {:^7} | {:^15} | {:^8} |'
          .format('Truck', 'Count', 'Pkg', 'Route', 'Miles', 'From', 'To', 'Status', 'Deadline'))
    print('-'*91)


def print_package_header():
    """Package header - matching Package class output

    Space Complexity O(1)
    Time Complexity O(1)"""
    print('-' * 66)
    print('| {:^3} | {:^5} | {:^8} | {:^8} | {:^15} | {:^8} |'
          .format('Pkg', 'Truck', 'Depart', 'ETA', 'Status', 'Deadline'))
    print('-'*66)
