section .data
    num1    dd  3
    num2    dd  4
    num3    dd  5
    result  dd  0
    out_fmt db  "結果: %d", 10, 0     ; "%d\n" 格式

section .text
    extern printf
    global main

main:
    ; 取 num1 進 eax
    mov eax, [num1]

    ; 乘上 num2 -> eax = eax * num2
    imul eax, [num2]

    ; 再乘上 num3 -> eax = eax * num3
    imul eax, [num3]

    ; 存到 result
    mov [result], eax

    ; 呼叫 printf 印出結果
    push eax                ; 結果當作參數
    push out_fmt            ; 格式字串當作參數
    call printf
    add esp, 8              ; 清除參數 (2個 4 bytes)

    ; 結束程式
    mov eax, 0
    ret
