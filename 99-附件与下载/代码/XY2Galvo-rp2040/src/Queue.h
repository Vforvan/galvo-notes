#pragma once
#include <cstdint>
#include "hardware/sync.h"

template<typename T, uint SIZE>
struct Queue
{
	static const uint MASK = SIZE - 1;
	static_assert(SIZE > 0 && (SIZE & MASK) == 0, "size must be a power of 2");

protected:
	T buffer[SIZE];
	volatile uint rp = 0;
	volatile uint wp = 0;

	static inline void copy (T* z, const T* q, uint n) {
		for (uint i=0; i<n; i++) { z[i] = q[i]; }
	}

	void copy_q2b(T* z, uint n) noexcept {
        uint rp_idx = this->rp & MASK;
        const T* q = buffer + rp_idx;
        uint n1 = SIZE - rp_idx;
        if (n <= n1) { copy(z, q, n); }
        else { copy(z, q, n1); copy(z + n1, buffer, n - n1); }
    }
	void copy_b2q(const T* q, uint n) noexcept {
        uint wp_idx = this->wp & MASK;
        T* z = buffer + wp_idx;
        uint n1 = SIZE - wp_idx;
        if (n <= n1) { copy(z, q, n); }
        else { copy(z, q, n1); copy(buffer, q + n1, n - n1); }
    }

public:
	uint avail() const noexcept { return wp - rp; }
	uint free() const noexcept { return SIZE - avail(); }
	T getc() { uint i=rp; T c = buffer[i++&MASK]; __dmb(); rp=i; return c; }
	void putc (T c) { uint i=wp; buffer[i++&MASK] = c; __dmb(); wp=i; }
    uint read (T* z, uint n) noexcept { n = min(n,avail()); copy_q2b(z,n); __dmb(); rp+=n; return n; }
    uint write (const T* q, uint n) noexcept { n = min(n,free()); copy_b2q(q,n); __dmb(); wp+=n; return n; }
};