#include <stdio.h>
#include <windows.h>

int main()
{
	__asm
	{
		push ebp
		mov ebp,esp
		xor edi,edi
		push edi
		sub esp,0ch
		mov byte ptr [ebp-0bh],6dh
		mov byte ptr [ebp-0ah],73h
		mov byte ptr [ebp-09h],76h
		mov byte ptr [ebp-08h],63h
        mov byte ptr [ebp-07h],72h
        mov byte ptr [ebp-06h],74h
        mov byte ptr [ebp-05h],2Eh
        mov byte ptr [ebp-04h],64h
        mov byte ptr [ebp-03h],6ch
		mov byte ptr [ebp-02h],6ch
		lea eax,[ebp-0bh]
		push eax
		mov ebx,0x7c801d77
		call ebx
		
		push ebp
		mov ebp,esp
		xor edi,edi
		push edi
		sub esp,08h
		mov byte ptr [ebp-09h],63h
		mov byte ptr [ebp-08h],61h
        mov byte ptr [ebp-07h],6Ch
        mov byte ptr [ebp-06h],63h
        mov byte ptr [ebp-05h],2Eh
        mov byte ptr [ebp-04h],65b
        mov byte ptr [ebp-03h],78h
		mov byte ptr [ebp-02h],65h
		lea eax,[ebp-09h]
		push eax
		mov ebx,0x77bf93c7
		call ebx
	}

}