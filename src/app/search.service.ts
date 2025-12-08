import { Injectable } from '@angular/core';
import { of, delay } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  search(query: string) {
    
    const fakeResults = [
      {
        title: `News: ${query} announces major update`,
        snippet: `${query} released new information that could impact its stock price.`,
        source: 'Reuters',
        date: '2025-11-12'
      },
      {
        title: `${query} quarterly report summary`,
        snippet: `Analysts react to ${query}'s latest financial performance.`,
        source: 'Bloomberg',
        date: '2025-11-10'
      }
    ];

    return of(fakeResults).pipe(delay(800)); // simulate 800ms delay
  }
}
