from CallCenter import CallCenter


if __name__ == '__main__':
    callCenter = CallCenter()
    callCenter.createOperator("A")
    callCenter.createOperator("B")
    callCenter.cmdloop()