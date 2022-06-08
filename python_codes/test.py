

"""PLEASE IGNORE THIS FILE"""


"""x = np.random.random_integers(1, 100, 5)
print(x)
plt.hist(x, bins=20)
plt.ylabel('No of times')
plt.show()"""





if __name__ == "__main__":

    text_file = open("sample.txt", "wt")
    STRING = ""
    #chart(occurance_list)
    for i in range(1,17326):
        STRING += (str(i) + "," + str(-i) + ",1\n")
    n = text_file.write(STRING)
    text_file.close()
