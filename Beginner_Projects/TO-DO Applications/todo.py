import pandas as pd
import os
def add_task(df):
    while True:
        task = input("Enter the task to add: ")
        if len(task)>0:
                break
        else :
            x=input("Enter non-empty Task!(enter) or exit (9) for not to add")
            if x=='9':
                return df
    if task in df['TO-DO'].values:
        print("Task already exists.")
    else:
        new_task = pd.DataFrame({'TO-DO': [task], 'Completed': [False]})
        df = pd.concat([df, new_task], ignore_index=True)
        df.to_csv('data.csv', index=False)
        print("Task added successfully.")
    return df
    
def remove_task(df, task):
    if df.empty:
        print("There are no tasks to be removed")
        return df
    if task not in df['TO-DO'].values:
        print("No such task existed")
    else:
        df=df[df['TO-DO']!=task]
    return df

def view_tasks(df):
    print(df)

def completed_tasks(df):
    if df.empty:
        print("There are no tasks to be Marked as Completed")
        return df
    task = input("Enter the task to be updated: ")
    if task not in df['TO-DO'].values:
        print("No such task existed to mark it as Completed")
    else:
        index=df[df['TO-DO']==task].index[0]
        df.loc[index,'Completed']=True
    return df

def main():
    path = '/home/c1/Documents/PYTHON_PROJECTS/Beginner_Projects/TO-DO Applications/data.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=['TO-DO','Completed'])  # Add your own column names
        df.to_csv(path, index=False)
        print("File not found. New file created.")
    df1=df
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View Tasks")
        print("4. Save Tasks")
        print("5. Completed Tasks")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")      
        if choice == '1':
            df=add_task(df)
        elif choice == '2':
            task = input("Enter the task to remove: ")
            df=remove_task(df, task)
        elif choice == '3':
            view_tasks(df)
        elif choice == '4':
            df.to_csv(path, index=False)
        elif choice == '5':
            df=completed_tasks(df)
        elif choice == '6':
            print(df1)
            print()
            print(df)
            if df1.equals(df):
                print("Exiting the application.")
                break
            else:
                print("You didnt save the file , please select 4 to save or else 6")
                choice = input("Choose an option (4/6): ")  
                if choice=='4':
                    df.to_csv(path, index=False)
                    df1=df
                elif choice=='6':
                    print("Exiting the application.")
                    break
        else:
            print("Invalid choice. Please try again.")
main()