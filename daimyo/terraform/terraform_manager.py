"""
Manages Terraform commands and environment setup
Author: Chris Vantine
"""
import subprocess


class TerraformManager:
    """
    Object for managing terraform commands and instances
    """
    def __init__(self, location):
        """
        Initialize the manager
        :param location: The path to the directory to work from
        """
        self.location = location
        self.plan_file = ""
        self.init()

    def init(self):
        """
        Initialize a terraform directory
        (terraform init -input=false)
        """
        # create the process
        process = subprocess.Popen(['terraform', 'init', '-input=false', self.location],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # print output
        output, error = process.communicate()
        print(output)
        print(error)

    def plan(self, filename):
        """
        Create a plan from the config
        :param filename: the file to print the plan out to
        """
        self.plan_file = self.location + "/" + filename
        process = subprocess.Popen(['terraform', 'plan', '-out=' + self.plan_file, "-input=false"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # print output
        output, error = process.communicate()
        print(output)
        print(error)
        print("[i] Plan file located at " + self.plan_file)

    def apply(self):
        """
        Apply the terraform config from the self generated plan
        """
        if self.plan_file == "":
            print("No plan file generated")
            return

        # create process
        process = subprocess.Popen(['terraform', 'apply', "-input=false", self.plan_file],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # print output
        output, error = process.communicate()
        print(output)
        print(error)

    def show(self):
        """
        Show state data
        """
        # create process
        process = subprocess.Popen(['terraform', 'show', self.location + "/" + "build.tf.state"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # print output
        output, error = process.communicate()
        print(output)
        print(error)
