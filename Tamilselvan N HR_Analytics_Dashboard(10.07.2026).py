# HR ANALYTICS SYSTEM 

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

sns.set_style("whitegrid")
plt.rcParams["figure.facecolor"] = "white"
random.seed(42)
np.random.seed(42)

DB_NAME = "hr_analytics_full.db"
TABLE_NAME = "employees"

# 1. GENERATE 100-EMPLOYEE DATAFRAME WITH 30 COLUMNS

def generate_employee_dataframe(n=100):
    departments = ["Sales", "IT", "HR", "Finance", "Operations", "Marketing", "R&D"]
    designations = ["Executive", "Senior Executive", "Team Lead", "Manager",
                    "Senior Manager", "Analyst", "Senior Analyst"]
    genders = ["Male", "Female"]
    marital_status_opts = ["Single", "Married"]
    education_opts = ["Diploma", "Bachelor's", "Master's", "PhD"]
    cities = ["Chennai", "Coimbatore", "Salem", "Madurai", "Trichy", "Erode", "Hosur"]
    states = {"Chennai": "Tamil Nadu", "Coimbatore": "Tamil Nadu", "Salem": "Tamil Nadu",
              "Madurai": "Tamil Nadu", "Trichy": "Tamil Nadu", "Erode": "Tamil Nadu",
              "Hosur": "Tamil Nadu"}
    employment_types = ["Full-Time", "Contract"]
    work_modes = ["Office", "Hybrid", "Remote"]
    business_travel_opts = ["None", "Rarely", "Frequently"]
    managers = ["R. Kumar", "S. Priya", "M. Anand", "V. Lakshmi", "K. Suresh", "N. Divya"]

    dept_base_salary = {"Sales": 32000, "IT": 55000, "HR": 30000, "Finance": 45000,
                         "Operations": 28000, "Marketing": 34000, "R&D": 60000}

    records = []
    for i in range(1, n + 1):
        dept = random.choice(departments)
        gender = random.choice(genders)
        age = random.randint(22, 58)
        experience = round(random.uniform(0.5, min(age - 21, 30)), 1)
        join_date = datetime(2026, 7, 10) - timedelta(days=int(random.uniform(30, experience * 365 + 30)))
        tenure_years = round((datetime(2026, 7, 10) - join_date).days / 365, 1)

        base = dept_base_salary[dept]
        salary = round(base + experience * 1700 + random.uniform(-4000, 6000), 2)
        bonus = round(salary * random.uniform(0.05, 0.20), 2)
        total_ctc = round((salary * 12) + bonus, 2)

        performance = round(random.uniform(2.0, 5.0), 1)
        kpi_score = round(random.uniform(50, 100), 1)
        satisfaction = round(random.uniform(1.0, 5.0), 1)
        overtime_hours = round(random.uniform(0, 25), 1)
        projects_handled = random.randint(1, 20)
        training_hours = random.randint(0, 60)
        leaves_taken = random.randint(0, 30)
        promotion_last_5 = random.choice(["Yes", "No"])
        distance_km = round(random.uniform(1, 45), 1)

        risk_score = (5 - performance) + (5 - satisfaction) + (overtime_hours / 10)
        attrition = "Yes" if (risk_score > 6 and random.random() < 0.55) or random.random() < 0.05 else "No"

        city = random.choice(cities)

        records.append({
            "emp_id": 1000 + i,
            "name": f"Employee_{i:03d}",
            "gender": gender,
            "age": age,
            "marital_status": random.choice(marital_status_opts),
            "department": dept,
            "designation": random.choice(designations),
            "education": random.choice(education_opts),
            "city": city,
            "state": states[city],
            "join_date": join_date.strftime("%Y-%m-%d"),
            "experience_years": experience,
            "tenure_years": tenure_years,
            "employment_type": random.choice(employment_types),
            "work_mode": random.choice(work_modes),
            "manager_name": random.choice(managers),
            "salary": salary,
            "bonus": bonus,
            "total_ctc": total_ctc,
            "performance_rating": performance,
            "kpi_score": kpi_score,
            "satisfaction_score": satisfaction,
            "overtime_hours": overtime_hours,
            "projects_handled": projects_handled,
            "training_hours": training_hours,
            "leaves_taken": leaves_taken,
            "promotion_last_5years": promotion_last_5,
            "distance_from_home_km": distance_km,
            "business_travel": random.choice(business_travel_opts),
            "attrition": attrition,
        })

    df = pd.DataFrame(records)
    assert df.shape[1] == 30, f"Expected 30 columns, got {df.shape[1]}"
    return df

# 2. CREATE DATABASE AND INSERT DATAFRAME

def create_database_from_dataframe(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print(f" Database '{DB_NAME}' created with table '{TABLE_NAME}' — "
          f"{len(df)} rows × {df.shape[1]} columns inserted.\n")


def insert_employee_manual():
    """Insert one additional real employee record manually into the same DB."""
    print("\n--- ADD NEW EMPLOYEE RECORD ---")
    emp_id = int(input("Employee ID (e.g. 2001): "))
    name = input("Name: ").strip()
    gender = input("Gender (Male/Female/Other): ").strip()
    age = int(input("Age: "))
    marital_status = input("Marital Status (Single/Married): ").strip()
    department = input("Department: ").strip()
    designation = input("Designation: ").strip()
    education = input("Education (Diploma/Bachelor's/Master's/PhD): ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    join_date = input("Join Date (YYYY-MM-DD): ").strip()
    experience_years = float(input("Experience (years): "))
    tenure_years = float(input("Tenure (years): "))
    employment_type = input("Employment Type (Full-Time/Contract): ").strip()
    work_mode = input("Work Mode (Office/Hybrid/Remote): ").strip()
    manager_name = input("Manager Name: ").strip()
    salary = float(input("Monthly Salary: "))
    bonus = float(input("Bonus: "))
    total_ctc = float(input("Total Annual CTC: "))
    performance_rating = float(input("Performance Rating (1-5): "))
    kpi_score = float(input("KPI Score (0-100): "))
    satisfaction_score = float(input("Satisfaction Score (1-5): "))
    overtime_hours = float(input("Overtime Hours (monthly): "))
    projects_handled = int(input("Projects Handled: "))
    training_hours = int(input("Training Hours: "))
    leaves_taken = int(input("Leaves Taken: "))
    promotion_last_5years = input("Promotion in Last 5 Years (Yes/No): ").strip()
    distance_from_home_km = float(input("Distance from Home (km): "))
    business_travel = input("Business Travel (None/Rarely/Frequently): ").strip()
    attrition = input("Attrition (Yes/No): ").strip().capitalize()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE_NAME} (
            emp_id, name, gender, age, marital_status, department, designation,
            education, city, state, join_date, experience_years, tenure_years,
            employment_type, work_mode, manager_name, salary, bonus, total_ctc,
            performance_rating, kpi_score, satisfaction_score, overtime_hours,
            projects_handled, training_hours, leaves_taken, promotion_last_5years,
            distance_from_home_km, business_travel, attrition
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (emp_id, name, gender, age, marital_status, department, designation,
          education, city, state, join_date, experience_years, tenure_years,
          employment_type, work_mode, manager_name, salary, bonus, total_ctc,
          performance_rating, kpi_score, satisfaction_score, overtime_hours,
          projects_handled, training_hours, leaves_taken, promotion_last_5years,
          distance_from_home_km, business_travel, attrition))
    conn.commit()
    conn.close()
    print(f" Employee '{name}' inserted successfully.\n")


def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

# 3. TEXT-BASED COMPARISON REPORTS

def report_overview(df):
    print("\n" + "=" * 72)
    print(" HR ANALYTICS — EXECUTIVE OVERVIEW")
    print("=" * 72)
    print(f"Total Employees          : {len(df)}")
    print(f"Total Columns            : {df.shape[1]}")
    print(f"Departments              : {df['department'].nunique()}")
    print(f"Average Age              : {df['age'].mean():.1f} yrs")
    print(f"Average Experience       : {df['experience_years'].mean():.1f} yrs")
    print(f"Average Tenure           : {df['tenure_years'].mean():.1f} yrs")
    print(f"Average Monthly Salary   : ₹{df['salary'].mean():,.2f}")
    print(f"Total Monthly Salary Bill: ₹{df['salary'].sum():,.2f}")
    print(f"Average Annual CTC       : ₹{df['total_ctc'].mean():,.2f}")
    print(f"Average Performance      : {df['performance_rating'].mean():.2f} / 5.0")
    print(f"Average KPI Score        : {df['kpi_score'].mean():.2f} / 100")
    print(f"Average Satisfaction     : {df['satisfaction_score'].mean():.2f} / 5.0")
    print(f"Average Overtime Hours   : {df['overtime_hours'].mean():.2f} hrs/month")
    print(f"Average Training Hours   : {df['training_hours'].mean():.1f} hrs")
    print(f"Promoted in Last 5 Yrs   : {(df['promotion_last_5years']=='Yes').mean()*100:.1f}%")
    print(f"Overall Attrition Rate   : {(df['attrition']=='Yes').mean()*100:.2f}%")
    print("=" * 72)


def report_department_comparison(df):
    print("\n--- DEPARTMENT-WISE COMPARISON ---")
    summary = df.groupby("department").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean"),
        Total_Salary=("salary", "sum"),
        Avg_CTC=("total_ctc", "mean"),
        Avg_Performance=("performance_rating", "mean"),
        Avg_Satisfaction=("satisfaction_score", "mean"),
        Attrition_Rate_pct=("attrition", lambda x: (x == "Yes").mean() * 100)
    ).round(2).sort_values("Avg_Salary", ascending=False)
    print(summary)
    print(f"\n Highest paying dept: {summary['Avg_Salary'].idxmax()}")
    print(f" Highest attrition dept: {summary['Attrition_Rate_pct'].idxmax()}")
    return summary


def report_designation_comparison(df):
    print("\n--- DESIGNATION-WISE COMPARISON ---")
    summary = df.groupby("designation").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean"),
        Avg_CTC=("total_ctc", "mean"),
        Avg_Performance=("performance_rating", "mean")
    ).round(2).sort_values("Avg_Salary", ascending=False)
    print(summary)
    return summary


def report_gender_comparison(df):
    print("\n--- GENDER-WISE COMPARISON ---")
    summary = df.groupby("gender").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean"),
        Avg_Performance=("performance_rating", "mean"),
        Avg_Satisfaction=("satisfaction_score", "mean")
    ).round(2)
    print(summary)
    return summary


def report_education_comparison(df):
    print("\n--- EDUCATION-WISE COMPARISON ---")
    summary = df.groupby("education").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean"),
        Avg_Performance=("performance_rating", "mean")
    ).round(2).sort_values("Avg_Salary", ascending=False)
    print(summary)
    return summary


def report_workmode_comparison(df):
    print("\n--- WORK MODE COMPARISON ---")
    summary = df.groupby("work_mode").agg(
        Headcount=("emp_id", "count"),
        Avg_Satisfaction=("satisfaction_score", "mean"),
        Avg_Performance=("performance_rating", "mean"),
        Attrition_Rate_pct=("attrition", lambda x: (x == "Yes").mean() * 100)
    ).round(2)
    print(summary)
    return summary


def report_employment_type_comparison(df):
    print("\n--- EMPLOYMENT TYPE COMPARISON ---")
    summary = df.groupby("employment_type").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean"),
        Avg_Performance=("performance_rating", "mean"),
        Attrition_Rate_pct=("attrition", lambda x: (x == "Yes").mean() * 100)
    ).round(2)
    print(summary)
    return summary


def report_city_comparison(df):
    print("\n--- CITY-WISE COMPARISON ---")
    summary = df.groupby("city").agg(
        Headcount=("emp_id", "count"),
        Avg_Salary=("salary", "mean")
    ).round(2).sort_values("Headcount", ascending=False)
    print(summary)
    return summary


def report_promotion_comparison(df):
    print("\n--- PROMOTION vs PERFORMANCE/ATTRITION ---")
    summary = df.groupby("promotion_last_5years").agg(
        Headcount=("emp_id", "count"),
        Avg_Performance=("performance_rating", "mean"),
        Avg_Satisfaction=("satisfaction_score", "mean"),
        Attrition_Rate_pct=("attrition", lambda x: (x == "Yes").mean() * 100)
    ).round(2)
    print(summary)
    return summary


def report_business_travel_comparison(df):
    print("\n--- BUSINESS TRAVEL vs ATTRITION ---")
    summary = df.groupby("business_travel").agg(
        Headcount=("emp_id", "count"),
        Avg_Satisfaction=("satisfaction_score", "mean"),
        Attrition_Rate_pct=("attrition", lambda x: (x == "Yes").mean() * 100)
    ).round(2)
    print(summary)
    return summary


def report_correlation(df):
    print("\n--- CORRELATION MATRIX (Key Numeric Factors) ---")
    cols = ["age", "experience_years", "tenure_years", "salary", "total_ctc",
            "performance_rating", "kpi_score", "satisfaction_score",
            "overtime_hours", "projects_handled", "training_hours"]
    corr = df[cols].corr().round(2)
    print(corr)
    strongest = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool)).stack().abs().idxmax()
    print(f"\n Strongest relationship: '{strongest[0]}' & '{strongest[1]}' "
          f"(r = {corr.loc[strongest]:.2f})")
    return corr


def report_attrition_analysis(df):
    print("\n--- ATTRITION DEEP-DIVE ---")
    left = df[df["attrition"] == "Yes"]
    stayed = df[df["attrition"] == "No"]
    print(f"Employees Left      : {len(left)}")
    print(f"Employees Retained  : {len(stayed)}")
    if len(left) > 0:
        print(f"Avg Perf (Left/Stay)     : {left['performance_rating'].mean():.2f} / "
              f"{stayed['performance_rating'].mean():.2f}")
        print(f"Avg Satisfaction (L/S)   : {left['satisfaction_score'].mean():.2f} / "
              f"{stayed['satisfaction_score'].mean():.2f}")
        print(f"Avg Overtime Hrs (L/S)   : {left['overtime_hours'].mean():.2f} / "
              f"{stayed['overtime_hours'].mean():.2f}")
        print(f"Avg Salary (L/S)         : ₹{left['salary'].mean():,.2f} / "
              f"₹{stayed['salary'].mean():,.2f}")
        print(f"Avg Tenure (L/S)         : {left['tenure_years'].mean():.2f} / "
              f"{stayed['tenure_years'].mean():.2f} yrs")
        print(f"\n💡 Highest attrition department: {left['department'].value_counts().idxmax()}")


def full_text_report(df):
    report_overview(df)
    report_department_comparison(df)
    report_designation_comparison(df)
    report_gender_comparison(df)
    report_education_comparison(df)
    report_workmode_comparison(df)
    report_employment_type_comparison(df)
    report_city_comparison(df)
    report_promotion_comparison(df)
    report_business_travel_comparison(df)
    report_correlation(df)
    report_attrition_analysis(df)

# 4. EXTENDED OVERALL VISUALIZATION DASHBOARD (KPI cards + all comparisons)

def overall_visualization(df):
    fig = plt.figure(figsize=(24, 34))
    gs = fig.add_gridspec(6, 3, hspace=0.55, wspace=0.3)
    fig.suptitle("HR ANALYTICS — FULL COMPARISON DASHBOARD (100 Employees)",
                 fontsize=24, fontweight="bold", y=1.005)

    #  Row 0: KPI SUMMARY CARDS (text-based)
    kpi_ax = fig.add_subplot(gs[0, :])
    kpi_ax.axis("off")
    kpis = [
        ("Total Employees", f"{len(df)}"),
        ("Avg Salary", f"₹{df['salary'].mean():,.0f}"),
        ("Total Salary Bill", f"₹{df['salary'].sum():,.0f}"),
        ("Avg CTC", f"₹{df['total_ctc'].mean():,.0f}"),
        ("Avg Performance", f"{df['performance_rating'].mean():.2f}/5"),
        ("Avg Satisfaction", f"{df['satisfaction_score'].mean():.2f}/5"),
        ("Avg KPI Score", f"{df['kpi_score'].mean():.1f}/100"),
        ("Attrition Rate", f"{(df['attrition']=='Yes').mean()*100:.1f}%"),
    ]
    n_kpi = len(kpis)
    box_w = 1.0 / n_kpi
    colors = ["#3F51B5", "#009688", "#FF9800", "#3F51B5", "#8E24AA", "#00897B", "#5D4037", "#E53935"]
    for idx, (label, value) in enumerate(kpis):
        x0 = idx * box_w
        kpi_ax.add_patch(plt.Rectangle((x0 + 0.005, 0.05), box_w - 0.01, 0.9,
                                        transform=kpi_ax.transAxes,
                                        facecolor=colors[idx % len(colors)], alpha=0.15,
                                        edgecolor=colors[idx % len(colors)], linewidth=1.5))
        kpi_ax.text(x0 + box_w / 2, 0.62, value, transform=kpi_ax.transAxes,
                    ha="center", va="center", fontsize=15, fontweight="bold",
                    color=colors[idx % len(colors)])
        kpi_ax.text(x0 + box_w / 2, 0.25, label, transform=kpi_ax.transAxes,
                    ha="center", va="center", fontsize=10.5, color="#333333")
    kpi_ax.set_xlim(0, 1)
    kpi_ax.set_ylim(0, 1)

    # Row 1 
    ax1 = fig.add_subplot(gs[1, 0])
    d = df["department"].value_counts()
    sns.barplot(x=d.values, y=d.index, ax=ax1, palette="viridis")
    ax1.set_title("Headcount by Department")

    ax2 = fig.add_subplot(gs[1, 1])
    sns.histplot(df["salary"], bins=20, kde=True, ax=ax2, color="steelblue")
    ax2.set_title("Monthly Salary Distribution")

    ax3 = fig.add_subplot(gs[1, 2])
    a = df["attrition"].value_counts()
    ax3.pie(a, labels=a.index, autopct="%1.1f%%", colors=["#4CAF50", "#E53935"], startangle=90)
    ax3.set_title("Attrition Split")

    # Row 2 
    ax4 = fig.add_subplot(gs[2, 0])
    sns.boxplot(data=df, x="department", y="salary", ax=ax4, palette="Set2")
    ax4.set_title("Salary Spread by Department")
    ax4.tick_params(axis="x", rotation=30)

    ax5 = fig.add_subplot(gs[2, 1])
    sns.scatterplot(data=df, x="performance_rating", y="salary", hue="attrition",
                     ax=ax5, palette={"Yes": "red", "No": "green"}, alpha=0.7)
    ax5.set_title("Performance vs Salary (Attrition)")

    ax6 = fig.add_subplot(gs[2, 2])
    cols = ["age", "experience_years", "salary", "performance_rating",
            "satisfaction_score", "overtime_hours"]
    sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm", ax=ax6, fmt=".2f")
    ax6.set_title("Correlation Heatmap")

    #  Row 3
    ax7 = fig.add_subplot(gs[3, 0])
    g = df.groupby("gender")["salary"].mean()
    sns.barplot(x=g.index, y=g.values, ax=ax7, palette="pastel")
    ax7.set_title("Avg Salary by Gender")

    ax8 = fig.add_subplot(gs[3, 1])
    e = df.groupby("education")["performance_rating"].mean().sort_values()
    sns.barplot(x=e.values, y=e.index, ax=ax8, palette="crest")
    ax8.set_title("Avg Performance by Education")

    ax9 = fig.add_subplot(gs[3, 2])
    w = df.groupby("work_mode")["satisfaction_score"].mean()
    sns.barplot(x=w.index, y=w.values, ax=ax9, palette="magma")
    ax9.set_title("Avg Satisfaction by Work Mode")

    #  Row 4 
    ax10 = fig.add_subplot(gs[4, 0])
    c = df["city"].value_counts()
    sns.barplot(x=c.values, y=c.index, ax=ax10, palette="rocket")
    ax10.set_title("Headcount by City")

    ax11 = fig.add_subplot(gs[4, 1])
    ar = df.groupby("department")["attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    sns.barplot(x=ar.values, y=ar.index, ax=ax11, palette="flare")
    ax11.set_title("Attrition Rate % by Department")

    ax12 = fig.add_subplot(gs[4, 2])
    sns.scatterplot(data=df, x="experience_years", y="total_ctc", hue="department",
                     ax=ax12, alpha=0.7, legend=False)
    ax12.set_title("Experience vs Total CTC")

    #  Row 5: Additional comparisons 
    ax13 = fig.add_subplot(gs[5, 0])
    desig = df.groupby("designation")["salary"].mean().sort_values()
    sns.barplot(x=desig.values, y=desig.index, ax=ax13, palette="cubehelix")
    ax13.set_title("Avg Salary by Designation")

    ax14 = fig.add_subplot(gs[5, 1])
    et = df.groupby("employment_type").agg(
        Avg_Salary=("salary", "mean"),
        Attrition_Rate=("attrition", lambda x: (x == "Yes").mean() * 100)
    )
    et["Avg_Salary"].plot(kind="bar", ax=ax14, color=["#26A69A", "#FF7043"])
    ax14.set_title("Avg Salary by Employment Type")
    ax14.tick_params(axis="x", rotation=0)

    ax15 = fig.add_subplot(gs[5, 2])
    bt = df.groupby("business_travel")["attrition"].apply(lambda x: (x == "Yes").mean() * 100)
    sns.barplot(x=bt.index, y=bt.values, ax=ax15, palette="Blues_d")
    ax15.set_title("Attrition Rate % by Business Travel")

    plt.tight_layout()
    plt.savefig("hr_overall_dashboard.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("\n Extended dashboard saved as 'hr_overall_dashboard.png'")

# 5. RUN EVERYTHING
df = generate_employee_dataframe(100)
create_database_from_dataframe(df)

print("Preview of generated data:")
print(df.head(), "\n")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}\n")

full_text_report(df)
overall_visualization(df)