from sim import run_sim
import matplotlib.pyplot as plt


windows = [2,6,8,9,10,11,12]

#run sim (numberOfWindows, priority, numOfRuns)
# without priority
df2 = run_sim(2, False, 1000)
df6 = run_sim(6,False,1000)
df8 = run_sim(8,False,1000)
df9 = run_sim(9,False,1000)
df10 = run_sim(10,False,1000)
df11= run_sim(11,False,1000)
df12 = run_sim(12,False,1000)

#with priority
df2_p = run_sim(2, True, 1000)
df6_p = run_sim(6,True,1000)
df8_p = run_sim(8,True,1000)
df9_p = run_sim(9,True,1000)
df10_p = run_sim(10,True,1000)
df11_p = run_sim(11,True,1000)
df12_p = run_sim(12,True,1000)

#grabbing average wait time of each customers depending on the number of windows
avg_wait_no_priority = [
    df2["average_wait"].mean(),
    df6["average_wait"].mean(),
    df8["average_wait"].mean(),
    df9["average_wait"].mean(),
    df10["average_wait"].mean(),
    df11["average_wait"].mean(),
    df12["average_wait"].mean(),
]

avg_wait_with_priority = [
    df2_p["average_wait"].mean(),
    df6_p["average_wait"].mean(),
    df8_p["average_wait"].mean(),
    df9_p["average_wait"].mean(),
    df10_p["average_wait"].mean(),
    df11_p["average_wait"].mean(),
    df12_p["average_wait"].mean(),
]

#grabbing number of cutomers not serving during working hours
not_served_no_priority = [
    df2["not_served_today"].mean(),
    df6["not_served_today"].mean(),
    df8["not_served_today"].mean(),
    df9["not_served_today"].mean(),
    df10["not_served_today"].mean(),
    df11["not_served_today"].mean(),
    df12["not_served_today"].mean(),
]

not_served_priority = [
    df2_p["not_served_today"].mean(),
    df6_p["not_served_today"].mean(),
    df8_p["not_served_today"].mean(),
    df9_p["not_served_today"].mean(),
    df10_p["not_served_today"].mean(),
    df11_p["not_served_today"].mean(),
    df12_p["not_served_today"].mean(),
]

#grabbing the average when cutomers wait over 15 minutes
wait_time_over_15_no_priority = [
    df2["pct_wait_over_15"].mean(),
    df6["pct_wait_over_15"].mean(),
    df8["pct_wait_over_15"].mean(),
    df9["pct_wait_over_15"].mean(),
    df10["pct_wait_over_15"].mean(),
    df11["pct_wait_over_15"].mean(),
    df12["pct_wait_over_15"].mean(),
]

wait_time_over_15_priority = [
    df2_p["pct_wait_over_15"].mean(),
    df6_p["pct_wait_over_15"].mean(),
    df8_p["pct_wait_over_15"].mean(),
    df9_p["pct_wait_over_15"].mean(),
    df10_p["pct_wait_over_15"].mean(),
    df11_p["pct_wait_over_15"].mean(),
    df12_p["pct_wait_over_15"].mean(),
]

#generating graphs 
##Graph 1: Average wait time with different number of windows
plt.figure()
plt.plot(windows, avg_wait_no_priority, marker="o", label="No Priority")
plt.plot(windows, avg_wait_with_priority, marker="o", linestyle="--", label="priority")
plt.xlabel("Number of Windows")
plt.ylabel("Average wait Time (minutes)")
plt.title("Average wait Time vs number of Windows ")
plt.legend()
plt.grid()
plt.savefig("avg_wait_vs_windows.png")
plt.show()

#graph 2: Number of cutomers not served based on number of windows 
plt.figure()
plt.plot(windows, not_served_no_priority, marker="o", label="No Priority")
plt.plot(windows, not_served_priority, marker="o", linestyle="--", label="Priority")
plt.xlabel("Number of Windows")
plt.ylabel("Averag of Customers Not Served")
plt.title("Customers Not Served vs Number of Windows")
plt.legend()
plt.grid()
plt.savefig("not_served_vs_windows.png")
plt.show()

#graph 3: Total percent of people waiting for over 15 minutes
plt.figure()
plt.plot(windows, wait_time_over_15_no_priority, marker="o", label="No Priority")
plt.plot(windows, wait_time_over_15_priority, marker="o", linestyle="--",label="Priority")
plt.xlabel("Number of Windows")
plt.ylabel("Percent of Customers Waiting More Than 15 min")
plt.title("Long Wait Percentage vs Number of Windows")
plt.legend()
plt.grid()
plt.savefig("wait_over_15_vs_windows.png")
plt.show()