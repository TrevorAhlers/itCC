import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-history',
  standalone: true,
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css'],
  imports: [CommonModule, HttpClientModule, RouterModule]
})
export class HistoryComponent implements OnInit {
  history: any[] = [];
  error = '';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.fetchHistory();
  }

  goToHome() {
    this.router.navigate(['/']);
  }

fetchHistory() {
  this.http.get<any[]>('http://localhost:5000/history/json').subscribe({
    next: (data) => {
      this.history = data; // store the JSON array in the component
    },
    error: (err) => {
      console.error('Error fetching history', err);
      this.error = 'Failed to fetch history';
    }
  });
}
}
