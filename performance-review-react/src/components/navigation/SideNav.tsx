import "./SideNav.css";

type SideNavProps = {
  setPage: (page: string) => void;
};

export default function SideNav({ setPage }: SideNavProps) {
  return (
    <div className="sidenav">
      <h2 className="sidenav-title">
        Performance Reviews
      </h2>

      <button className="menu-item active" onClick={() => setPage("dashboard")}>
        🏠 Dashboard
      </button>

      <button className="menu-item" onClick={() => setPage("employees")}>
        👥 Employees
      </button>

      <button className="menu-item" onClick={() => setPage("reviews")}>
        📝 Reviews
      </button>

      <button className="menu-item" onClick={() => setPage("submit-review")}>
        ➕ Submit Review
      </button>
    </div>
  );
}