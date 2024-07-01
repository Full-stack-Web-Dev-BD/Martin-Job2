import schedule
import time
from datetime import datetime, timedelta

# Import your functions for data insert/update and profit calculation
from UK.C_to_C_sp_gsl_L2 import fetch_and_update_sp_gsl_lookup2
from UK.C_to_C_sp_upc import fetch_and_update_sp_upc_lookup
from UK.C_to_C_sp_upc_L2 import fetch_and_update_sp_upc_lookup2
from UK.Profit_L1 import calculateProfit_sp_upc_lookup1
from UK.Profit_L2 import calculateProfit_sp_upc_lookup2
from UK.Profit_sp_gsl_L2 import calculateProfit_sp_gsl_lookup2
from US.C_to_C_sp_upc import fetch_and_update_sp_upc_lookup as fetch_and_update_us_sp_upc_lookup
from US.Profit import fetch_and_update_us_profit

# Function to print details and time remaining
def print_schedule_details():
    current_time = datetime.now()
    print(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} GMT")
    print("\nScheduled Jobs:")
    for job in schedule.jobs:
        job_func = job.job_func.__name__
        next_run = job.next_run.strftime('%Y-%m-%d %H:%M:%S') if job.next_run else "None (Job finished)"
        time_remaining = job.next_run - current_time if job.next_run else timedelta(seconds=0)
        print(f"Function: {job_func}")
        print(f"Scheduled Time: {next_run} (Time Remaining: {time_remaining})")
        print("---")

# Define a flag to ensure initialization runs only once
initialized = False

# Function to initialize and run all jobs once
def initialize_and_run_jobs():
    global initialized
    if not initialized:
        # Run each job once
        job_fetch_and_update_sp_upc_lookup()
        job_fetch_and_update_sp_upc_lookup2()
        job_fetch_and_update_sp_gsl_lookup2()
        job_calculateProfit_sp_upc_lookup1()
        job_calculateProfit_sp_upc_lookup2()
        job_calculateProfit_sp_gsl_lookup2()
        job_fetch_and_update_us_sp_upc_lookup()
        job_fetch_and_update_us_profit()
        
        # Set initialized flag to True
        initialized = True

# Schedule jobs
schedule.every().day.at("04:00").do(job_fetch_and_update_sp_upc_lookup)
schedule.every().day.at("04:15").do(job_fetch_and_update_sp_upc_lookup2)
schedule.every().day.at("04:20").do(job_fetch_and_update_sp_gsl_lookup2)

schedule.every().day.at("04:00").do(job_calculateProfit_sp_upc_lookup1)
schedule.every().day.at("04:15").do(job_calculateProfit_sp_upc_lookup2)
schedule.every().day.at("04:20").do(job_calculateProfit_sp_gsl_lookup2)

schedule.every().day.at("04:00").do(job_fetch_and_update_us_sp_upc_lookup)
schedule.every().day.at("04:00").do(job_fetch_and_update_us_profit)

# Print initial schedule details
print_schedule_details()

# Initialize and run all jobs once
initialize_and_run_jobs()

# Run the scheduler
while True:
    schedule.run_pending()
    print_schedule_details()
    time.sleep(60)  # Check every minute
