int main() {
    int a = 2;
    int b = 3;
    int c = 4;
    int d = (a + b) * c;  /* (2+3)*4 = 20 */
    int e = d / (b - a);  /* 20/(3-2) = 20 */
    int f = (a * b) + (c * d);  /* (2*3)+(4*20) = 86 */
    printf("%d", d);
    printf("%d", e);
    printf("%d", f);
    return 0;
} 