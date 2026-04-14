import numpy as np
import pandas as pd
import heapq

minPerDay = 480
numOfCustomers = 160

# no seed, generates random values each time
def daySim(numOfWindows, priority, seed):
    if seed is not None:
        np.random.seed(seed)

    #generating the time cusomers arrive
    arrivals = np.sort(np.random.uniform(0,minPerDay, numOfCustomers))

    #generating how long customers take to complete the task and determine how much the task needs
    # setting 6  minutes for each task per customer
    work_unit = np.clip(np.random.normal(5, 0.5, numOfCustomers), 5, 15)
    service_time = work_unit * 6

    #grabbing stats like arrival times, how long task is predicted to takes, how long the task actually took
    customers= [] 
    for i in range(numOfCustomers):
        customers.append({
            "id": i,
            "arrival": arrivals[i],
            "work_unit": work_unit[i],
            "service_time": service_time[i]
        })

    # if priority is set to True, we sort customs by how long their task will take 
    # tie breaked => arival time 
    priorityQ = [(0,w) for w in range(numOfWindows)]
    heapq.heapify(priorityQ)
    results = []

    if not priority:
        for c in customers:
            available_time, window_id = heapq.heappop(priorityQ)
            start_time = max(c["arrival"], available_time)
            end_time = start_time + c["service_time"]
            wait_time = start_time - c["arrival"]

            results.append({
                "id":c["id"],
                "arrival": c["arrival"],
                "work_units": c["work_unit"],
                "service_time": c["service_time"],
                "window": window_id,
                "start": start_time,
                "end": end_time,
                "wait": wait_time,
                "served_today": end_time <= minPerDay
            })
            heapq.heappush(priorityQ, (end_time, window_id))
    else: #with priority
        #priority handeling 
        waiting = []
        i = 0
        current_time = 0

        while i < numOfCustomers or waiting:
            #add all customers who arrived by currect_time
            while i < numOfCustomers and customers[i]["arrival"] <= current_time:
                #set priority by smaller work units 
                heapq.heappush(waiting, (customers[i]["work_unit"], customers[i]["arrival"], customers[i]))
                i += 1

            # get next open server
            available_time, window_id = heapq.heappop(priorityQ)
            current_time = max(current_time, available_time)

            while i < numOfCustomers and customers[i]["arrival"] <= current_time:
                heapq.heappush(waiting, (customers[i]["work_unit"], customers[i]["arrival"], customers[i]))
                i += 1
            
            if waiting:
                _, _, c = heapq.heappop(waiting)
                start_time = max(c["arrival"], current_time)
                end_time = start_time + c["service_time"]
                wait_time = start_time - c["arrival"]

                results.append({
                    "id":c["id"],
                    "arrival": c["arrival"],
                    "work_units": c["work_unit"],
                    "service_time": c["service_time"],
                    "window": window_id,
                    "start": start_time,
                    "end": end_time,
                    "wait": wait_time,
                    "served_today": end_time <= minPerDay
                })

                heapq.heappush(priorityQ, (end_time, window_id))
                current_time = start_time
            else: 
                #if no one is waiting then go to the next arrival if possible
                if i < numOfCustomers:
                    current_time = max(current_time, customers[i]["arrival"])
                    heapq.heappush(priorityQ, (current_time, window_id))
                else: 
                    heapq.heappush(priorityQ, (available_time, window_id))
                    break
    df = pd.DataFrame(results)

    summary = {
        "average_wait": df["wait"].mean(),
        "median_wait": df["wait"].median(),
        "max_wait": df["wait"].max(),
        #what # of task waited for more than 15 (deterime if customers waited for too long)
        "pct_wait_over_15": (df["wait"] > 15).mean() * 100, 
        "served_today": df["served_today"].sum(),
        "not_served_today": (~df["served_today"]).sum(),
        "avg_service_time": df["service_time"].mean()
    }

    return df, summary


# running the simulation n time numOfRuns 
def run_sim(num_windows, priority, numOfRuns):
    summaries = []
    for r in range(numOfRuns):
        _, summary = daySim(numOfWindows=num_windows, priority=priority, seed=None)
        summaries.append(summary)
    return pd.DataFrame(summaries)

if __name__ == "__main__":
    #running simulations with different windows and or with priority
    #average wait time
    df2 = run_sim(num_windows=2, priority=False, numOfRuns=1000)
    df6 = run_sim(num_windows=6, priority=False, numOfRuns=1000)
    df8 = run_sim(num_windows=8, priority=False, numOfRuns=1000)
    df9 = run_sim(num_windows=9, priority=False, numOfRuns=1000)
    df10 = run_sim(num_windows=10, priority=False, numOfRuns=1000)
    df11 = run_sim(num_windows=11, priority=False, numOfRuns=1000)
    df12 = run_sim(num_windows=12, priority=False, numOfRuns=1000)

    # same number of windows with pority this time 
    df2_1 = run_sim(num_windows=2, priority=True, numOfRuns=1000)
    df6_1 = run_sim(num_windows=6, priority=True, numOfRuns=1000)
    df8_1 = run_sim(num_windows=8, priority=True, numOfRuns=1000)
    df9_1 = run_sim(num_windows=9, priority=True, numOfRuns=1000)
    df10_1 = run_sim(num_windows=10, priority=True, numOfRuns=1000)
    df11_1 = run_sim(num_windows=11, priority=True, numOfRuns=1000)
    df12_1 = run_sim(num_windows=12, priority=True, numOfRuns=1000)

    print("\nAverage Time:")
    print("Without Priority")
    print("Average wait time with 2 windows: ", round(df2["average_wait"].mean(), 2))
    print("Average wait time with 6 windows: ", round(df6["average_wait"].mean(), 2))
    print("Average wait time with 8 windows: ", round(df8["average_wait"].mean(), 2))
    print("Average wait time with 9 windows: ", round(df9["average_wait"].mean(), 2))
    print("Average wait time with 10 windows: ", round(df10["average_wait"].mean(), 2))
    print("Average wait time with 11 windows: ", round(df11["average_wait"].mean(), 2))
    print("Average wait time with 12 windows: ", round(df12["average_wait"].mean(), 2))

    print("With Priority")
    print("Average wait time with 2 windows and priority: ", round(df2_1["average_wait"].mean(), 2))
    print("Average wait time with 6 windows and priority: ", round(df6_1["average_wait"].mean(), 2))
    print("Average wait time with 8 windows and priority: ", round(df8_1["average_wait"].mean(), 2))
    print("Average wait time with 9 windows and priority: ", round(df9_1["average_wait"].mean(), 2))
    print("Average wait time with 10 windows and priority: ", round(df10_1["average_wait"].mean(), 2))
    print("Average wait time with 11 windows and priority: ", round(df11_1["average_wait"].mean(), 2))
    print("Average wait time with 12 windows and priority: ", round(df12_1["average_wait"].mean(), 2))



    print("\n\nNot Served:")
    print("w/o priority")
    print("Average number of customers not served with 2 windows: ", round(df2["not_served_today"].mean(), 2))
    print("Average number of customers not served with 6 windows: ", round(df6["not_served_today"].mean(), 2))
    print("Average number of customers not served with 8 windows: ", round(df8["not_served_today"].mean(), 2))
    print("Average number of customers not served with 9 windows: ", round(df9["not_served_today"].mean(), 2))
    print("Average number of customers not served with 10 windows: ", round(df10["not_served_today"].mean(), 2))
    print("Average number of customers not served with 11 windows: ", round(df11["not_served_today"].mean(), 2))
    print("Average number of customers not served with 12 windows: ", round(df12["not_served_today"].mean(), 2))

    print("w/ priority")
    print("Average number of customers not served with 2 windows and priority: ", round(df2_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 6 windows and priority: ", round(df6_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 8 windows: and priority ", round(df8_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 9 windows: and priority ", round(df9_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 10 windows: and priority ", round(df10_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 11 windows: and priority ", round(df11_1["not_served_today"].mean(), 2))
    print("Average number of customers not served with 12 windows: and priority ", round(df12_1["not_served_today"].mean(), 2))


    print("\n\nAverage Number of Customers waiting 15min or more:")
    print("w/o priority")
    print("Average number of customers waiting at least 15 minutes with 2 windows: ", round(df2["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 6 windows: ", round(df6["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 8 windows: ", round(df8["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 9 windows: ", round(df9["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 10 windows: ", round(df10["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 11 windows: ", round(df11["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 12 windows: ", round(df12["pct_wait_over_15"].mean(), 2))

    print("w/ priority")
    print("Average number of customers waiting at least 15 minutes with 2 windows and priority: ", round(df2_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 6 windows and priority: ", round(df6_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 8 windows and priority: ", round(df8_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 9 windows and priority: ", round(df9_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 10 windows and priority: ", round(df10_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 11 windows and priority: ", round(df11_1["pct_wait_over_15"].mean(), 2))
    print("Average number of customers waiting at least 15 minutes with 12 windows and priority: ", round(df12_1["pct_wait_over_15"].mean(), 2))

