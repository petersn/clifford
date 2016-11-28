// Clifford attractors.

using namespace std;
#include <iostream>
#include <random>

#include <stdint.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#define WIDTH 246
#define HEIGHT 336

#define TESTS 100
#define ITERATIONS 1000
#define TRAJECTORIES 1000

float random_float() {
	static uint64_t x = 0xe322b74f1e216cbe;
	x = (((x >> 4) ^ (x >> 3) ^ (x >> 1) ^ x) << 63) | (x >> 1);
	uint32_t temp = 0x3f800000u | (x & ((1<<23)-1));
	return (*reinterpret_cast<float*>(&temp)) - 1.0f;
}

int main(int argc, char** argv) {
	std::random_device rd;
	std::mt19937 e2(rd());
	std::uniform_real_distribution<> dist(-2, 2);

	assert(argc == 2);

	float fill_fraction;
	sscanf(argv[1], "%f", &fill_fraction);

	char* array = new char[WIDTH * HEIGHT]();

	float best_a = 0, best_b = 0, best_c = 0, best_d = 0;
	int best_score = -1;

	for (int i = 0; i < TESTS; i++) {
		float a, b, c, d;
		a = dist(e2);
		b = dist(e2);
		c = dist(e2);
		d = dist(e2);

		memset(array, 0, WIDTH * HEIGHT);

		for (int trajectory = 0; trajectory < TRAJECTORIES; trajectory++) {
			float x = random_float() * 2.0 - 1.0, y = random_float() * 2.0 - 1.0;

			for (int iterations = 0; iterations < ITERATIONS; iterations++) {
				float xn = sinf(a * y) + c * cosf(a * x);
				float yn = sinf(b * x) - d * cosf(b * y);
				x = xn;
				y = yn;

//				float screen_x = x / 5.0 + 0.5, screen_y = y / 5.0 + 0.5;

//				int x_index = screen_x * WIDTH, y_index = screen_y * WIDTH;
				float screen_x = x / 3.5 + 0.5, screen_y = y / 3.5 + 0.5;
				int x_index = screen_x * WIDTH, y_index = screen_y * HEIGHT;

				if (iterations > 10 && 0 <= x_index && x_index < WIDTH && 0 <= y_index && y_index < HEIGHT)
					array[x_index + WIDTH * y_index] = 1;
			}
		}

		// Compute a rough heuristic score.
		int score = 0;
		for (int y = 0; y < HEIGHT; y++)
			for (int x = 0; x < WIDTH; x++)
				score += array[x + WIDTH * y];

		// REVERSAL THRESHOLD:
		float reversal = WIDTH * HEIGHT * fill_fraction;
		if (score > reversal)
			score = 2 * reversal - score;

		// Maximize.
		if (score > best_score) {
			best_score = score;
			best_a = a;
			best_b = b;
			best_c = c;
			best_d = d;
		}
	}

	cout << best_a << "\n" << best_b << "\n" << best_c << "\n" << best_d << "\n";
	cout << "Score: " << best_score << endl;
}

