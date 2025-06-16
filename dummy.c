#include <stdio.h>
#include "lib/func.h"

/* forward declarations */
int  f1(void);
void f2(int a, int b);
// void f3(void);
// void f4(void);
void f6 (int x);
void f7(int x);
void f8(void);
void callback_func(void);
void register_event_handler(void (*callback)(void));

void callback_func() {
    int a = 0;
    return;
}

void register_event_handler(void (*callback)(void)) {
    callback();
}

int main(void)
{
    int x = f1();
    f6(x);
    register_event_handler(callback_func);
    return 0;
}


int f1(void)
{
    f2 (0, 0);
    return 0;
}

void f2 (int a, int b)
{
    
    if (a > b || a < 13)
    {
        f1();
    }
    f3();
    puts("test");

}

// void f3(void)
// {
//     f4();
// }

// void f4(void)
// {
//     /* no-op */
// }

void f6(int x)
{
    x = x + 1;
    f7(x);
}

void f7(int x)
{
    x = 3;
    f8();
}

void f8(void)
{
    f6(0); 
}
