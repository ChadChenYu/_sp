00000000 <power2>:
   0:   55                      push   ebp
   1:   89 e5                   mov    ebp,esp
   3:   83 ec 10                sub    esp,0x10
   6:   c7 45 fc 01 00 00 00    mov    DWORD PTR [ebp-0x4],0x1
   d:   c7 45 f8 01 00 00 00    mov    DWORD PTR [ebp-0x8],0x1
  14:   8b 45 f8                mov    eax,DWORD PTR [ebp-0x8]
  17:   3b 45 08                cmp    eax,DWORD PTR [ebp+0x8]
  1a:   7f 1a                   jg     36 <power2+0x36>
  1c:   8b 45 fc                mov    eax,DWORD PTR [ebp-0x4]
  1f:   c1 e0 01                shl    eax,1
  22:   89 45 fc                mov    DWORD PTR [ebp-0x4],eax
  25:   83 45 f8 01             add    DWORD PTR [ebp-0x8],0x1
  29:   eb e9                   jmp    14 <power2+0x14>
  2b:   8b 45 fc                mov    eax,DWORD PTR [ebp-0x4]
  2e:   c9                      leave
  2f:   c3                      ret
