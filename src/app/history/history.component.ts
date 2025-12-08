import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css'],
})
export class HistoryComponent implements OnInit {
  history: any[] = [];
  loading = false;
  error: string | null = null;

  constructor(private http: HttpClient, private router: Router) {}

  goToHome() {
    this.router.navigate(['/']);
  }

  ngOnInit(): void {
    this.loading = true;
    this.http.get<any[]>('http://localhost:5000/history/json').subscribe({
      next: (data) => {
        this.history = data.reverse(); 
        this.loading = false;
      },
      error: (err) => {
        this.error = "Could not load history";
        this.loading = false;
        console.error(err); // <--- add this to see actual error
      }
    });
  }

  exportCSV() {
  if (!this.history || this.history.length === 0) {
    return;
  }

  // Create CSV header
  const header = ['Time', 'Ticker', 'Price', 'Change', 'Day Range', 'Volume'];
  const rows = this.history.map(item => [
    item.time,
    item.ticker,
    item.price,
    item.change,
    item.day_range,
    item.volume
  ]);

  // Combine header + rows
  const csvContent = [
    header.join(','), // header row
    ...rows.map(e => e.map(v => `"${v}"`).join(',')) // wrap values in quotes
  ].join('\n');

  // Create a blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.setAttribute('href', url);
  a.setAttribute('download', `stock_history_${new Date().toISOString()}.csv`);
  a.click();
  window.URL.revokeObjectURL(url);
}
}
