import matplotlib.pyplot as plt


class Visualization:
    @staticmethod
    def visualize(labels, results, epochs):
        colors = ["-r", "-g", "-b", "-c", "--r", "--g", "--b", "--c"]
        for label, result, color in zip(labels, results, colors):
            xs = list(range(0, epochs))
            ys = [i for i in result]

            plt.plot(xs, ys, color, label="{}".format(label))

        plt.xlim(0, epochs)
        plt.xlabel("Epoch")
        plt.ylabel("Fitness score")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=10)
        plt.show()
