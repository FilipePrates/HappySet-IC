def main():
    graph = input('Gerar qual grafo?')
    if graph == 'star':
        for n in range(1,16):
            f = open("/home/cliente/Code/UFRJ/happySet/star_" + str(2**n) + ".txt", "w")   # 'r' for reading and 'w' for writing
            f.write(str(2**n) + " " + str(2**n - 1) + "\n")    # Write inside file 
            for e in range(1, 2**n):
                print("2**n:", 2**n, "e:", e)
                f.write("0 " + str(e) + "\n")    # Write inside file 
            f.write("end")
            f.close() 
if __name__ == "__main__":
    main()
