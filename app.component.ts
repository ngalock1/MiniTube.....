import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  template: `
    @if (!isLandingPage) {
      <app-navbar></app-navbar>
    }
    <main [class.main-content]="!isLandingPage">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    .main-content {
      min-height: calc(100vh - var(--navbar-height));
      margin-top: var(--navbar-height);
    }
  `]
})
export class AppComponent implements OnInit {
  constructor(private authService: AuthService, private router: Router) {}

  get isLandingPage(): boolean {
    return this.router.url === '/';
  }

  ngOnInit(): void {
    this.authService.checkStoredToken();
  }
}
