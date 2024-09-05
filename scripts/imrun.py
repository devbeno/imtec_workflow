import os
import subprocess
import time

from invoke import Collection, Program, task

# Define the collection object for tasks
namespace = Collection()


def stream_logs(machine_name, delay=2, max_iterations=None):
    """
    Stream logs from the ORB machine while a process is running.

    Args:
        machine_name (str): Name of the machine to stream logs from.
        delay (int): Time delay between log retrievals.
        max_iterations (int): For testing, limits the number of iterations. Defaults to None (infinite loop).
    """
    print(f"Streaming logs from machine: {machine_name}")
    iteration = 0
    while True:
        try:
            subprocess.run(f"orb logs {machine_name} --all", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Error retrieving logs. Exiting...")
            break
        time.sleep(delay)

        # For testing, stop after a certain number of iterations
        if max_iterations is not None:
            iteration += 1
            if iteration >= max_iterations:
                break


def run_command(command):
    try:
        if isinstance(command, str):
            command = command.split(" ")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{e.cmd}' failed with return code {e.returncode}")
        raise


def run_command_output(command):
    """
    Run a shell command and return its output as a list of lines.
    """
    try:
        print(f"Running command: {command}")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8").splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return []


WORKBASE = os.environ.get("WORKBASE")
if not WORKBASE:
    raise EnvironmentError(
        "WORKBASE is not set in your environment. Please ensure it's defined in your profile."
    )


def load_env(machine_name):
    env_file = f"{WORKBASE}/{machine_name}/.env"
    if os.path.exists(env_file):
        print(f"Loading environment variables from {env_file}")
        with open(env_file) as f:
            for line in f:
                if not line.strip() or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    else:
        raise FileNotFoundError(f"Environment file {env_file} not found.")


@task
def generate_env(c):
    """
    Run the shell script to generate the .env file for the project.
    """
    script_path = "./projects/generate-env"
    if os.path.exists(script_path):
        subprocess.run(["bash", script_path], check=True)
    else:
        print(f"Error: {script_path} not found.")


@task
def build(c):
    """
    Build the ORB machine and initialize it using environment variables.
    """
    machine_name = input("Enter the project name: ")

    generate_env(c)
    load_env(machine_name)

    distro = os.environ.get("DISTRO", "ubuntu")
    version = os.environ.get("VERSION", "jammy")
    arch = os.environ.get("ARCH", "amd64")
    frappe_user = os.environ.get("FRAPPE_USER", "frappe")

    create_command = f"orb create -a {arch} {distro}:{version} {machine_name} -u {frappe_user}"
    print(f"Running command: {create_command}")
    create_process = subprocess.Popen(create_command, shell=True)

    stream_logs(machine_name)
    create_process.wait()

    run_command(f"orb push -m {machine_name} {WORKBASE}/{machine_name}/.env /home/{frappe_user}/frappe_env")
    run_command(f"orb push -m {machine_name} ./projects/frappe_setup /home/{frappe_user}/")

    setup_command = f"orb run -m {machine_name} -u {frappe_user} bash /home/{frappe_user}/frappe_setup"
    setup_process = subprocess.Popen(setup_command, shell=True)

    print("Streaming logs during Frappe setup...")
    stream_logs(machine_name)
    setup_process.wait()


@task
def destroy(c):
    """
    Destroy the ORB machine and remove its project directory.
    """
    machine_name = input("Enter the project name: ")
    if not machine_name:
        print("Project name cannot be empty.")
        return

    try:
        run_command(f"orb delete {machine_name} --force")
    except subprocess.CalledProcessError as e:
        if "machine not found" in str(e):
            print(f"Machine '{machine_name}' not found, proceeding to remove the project directory.")
        else:
            print(f"Error deleting machine: {e}")
            return

    project_path = f"{WORKBASE}/{machine_name}"
    run_command(f"rm -rf {project_path}")
    print(f"Project directory {project_path} removed successfully.")


@task
def stop(c):
    """
    Stop the ORB machine.
    """
    machine_name = input("Enter the project name: ")
    load_env(machine_name)
    run_command(f"orb stop {os.environ.get('MACHINE_NAME')}")


@task
def list(c):
    """
    List the ORB machines and corresponding project directories in the WORKBASE.
    """
    machine_names = run_command_output("orb list -q")
    if not machine_names:
        print("No ORB machines found.")
        return

    print(f"ORB machines found: {', '.join(machine_names)}")

    for machine_name in machine_names:
        project_path = f"{WORKBASE}/{machine_name}"
        if os.path.exists(project_path):
            print(f"Listing project directory for machine: {machine_name}")
            try:
                run_command(f"ls -la {project_path}")
            except subprocess.CalledProcessError:
                print(f"Error listing directory: {project_path}")
        else:
            print(f"Skipping non-existent project directory: {project_path}")


namespace.add_task(generate_env)
namespace.add_task(build)
namespace.add_task(destroy)
namespace.add_task(stop)
namespace.add_task(list)


def main():
    program = Program(namespace=namespace)
    program.run()


if __name__ == "__main__":
    main()
