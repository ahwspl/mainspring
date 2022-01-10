"""A sample job that prints string."""

from mainspring import job


class DemoJob(job.JobBase):

    @classmethod
    def meta_info(cls):
        """

        :return:
        """
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': 'This will print a string in your shell. Check it out!',
            'arguments': [
                # argument1
                {
                    'type': 'string', 'description': 'First argument'
                },

                # argument2
                {
                    'type': 'string', 'description': 'Second argument'
                }
            ],
            'example_arguments': '["first argument AAA", "second argument BBB"]'
        }

    @staticmethod
    def run(argument1, argument2, *args, **kwargs):
        """

        :param argument1:
        :param argument2:
        :param args:
        :param kwargs:
        :return:
        """
        print('Hello from DemoJob! Argument1: %s, Argument2: %s' % (argument1, argument2))
        return [argument1, argument2]


if __name__ == "__main__":
    # You can easily test this job here
    job = DemoJob.create_test_instance()
    job.run(123, 456)
