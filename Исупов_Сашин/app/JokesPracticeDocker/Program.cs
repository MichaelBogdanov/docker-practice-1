namespace JokesPracticeDocker
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();

            var app = builder.Build();

            app.UseAuthorization();
            app.MapControllers();

            // 🔥 Добавляем порт из переменной окружения или 5000 по умолчанию

            app.Run();
        }
    }
}