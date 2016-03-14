// Clifford attractors.

#include <stdint.h>
#include <unistd.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

#define WIDTH 3200 //768
#define HEIGHT 3200 //768
#define kITERATIONS 500

float random_float() {
	static uint64_t x = 0xe322b74f1e216cbe;
	x = (((x >> 4) ^ (x >> 3) ^ (x >> 1) ^ x) << 63) | (x >> 1);
	uint32_t temp = 0x3f800000u | (x & ((1<<23)-1));
	return (*reinterpret_cast<float*>(&temp)) - 1.0f;
}

int main(int argc, char** argv) {
	assert(argc == 10);

	int sizes[] = {WIDTH, HEIGHT};
	write(1, sizes, 8);

	float* array = new float[WIDTH * HEIGHT];
	for (int i = 0; i < WIDTH * HEIGHT; i++)
		array[i] = 0.0;

	int trajectory_count;
	float start_x, start_y, end_x, end_y;
	float a, b, c, d;
	sscanf(argv[1], "%i", &trajectory_count);

//	sscanf(argv[2], "%f", &start_x);
//	sscanf(argv[3], "%f", &start_y);
//	sscanf(argv[4], "%f", &end_x);
//	sscanf(argv[5], "%f", &end_y);

	sscanf(argv[6], "%f", &a);
	sscanf(argv[7], "%f", &b);
	sscanf(argv[8], "%f", &c);
	sscanf(argv[9], "%f", &d);

	for (int trajectory = 0; trajectory < trajectory_count; trajectory++) {
		float lerp = trajectory / (float)(trajectory_count - 1);
//		float x = (1 - lerp) * start_x + lerp * end_x;
//		float y = (1 - lerp) * start_y + lerp * end_y;
		float x = random_float() * 2.0 - 1.0, y = random_float() * 2.0 - 1.0;

		for (int iterations = 0; iterations < (1000 * kITERATIONS); iterations++) {
			float xn = sinf(a * y) + c * cosf(a * x);
			float yn = sinf(b * x) - d * cosf(b * y);
			x = xn;
			y = yn;

			float screen_x = x / 5.0 + 0.5, screen_y = y / 5.0 + 0.5;

			int x_index = screen_x * WIDTH, y_index = screen_y * WIDTH;
			if (0 <= x_index && x_index < WIDTH && 0 <= y_index && y_index < HEIGHT)
				array[x_index + WIDTH * y_index] += 1.0;
		}
	}

	for (int i = 0; i < WIDTH * HEIGHT; i++)
		array[i] *= 1.0 / trajectory_count;

	write(1, array, sizeof(float) * WIDTH * HEIGHT);
	delete array;
}

