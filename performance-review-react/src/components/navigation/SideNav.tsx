import "./SideNav.css";

type SideNavProps = {
  page: string;
  setPage: (page: string) => void;
};

const menuItems = [
  { key: "dashboard", label: "🏠 Dashboard" },
  { key: "employees", label: "👥 Employees" },
  { key: "reviews", label: "📝 Reviews" },
  { key: "submit-review", label: "➕ Submit Review" },
];

export default function SideNav({ page, setPage }: SideNavProps) {
  return (
    <div className="sidenav">
      <h2 className="sidenav-title">
        Performance Reviews
      </h2>

      {menuItems.map((item) => (
        <button
          key={item.key}
          className={page === item.key ? "menu-item active" : "menu-item"}
          onClick={() => setPage(item.key)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
